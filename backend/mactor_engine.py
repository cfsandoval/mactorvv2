"""
MACTOR (Matriz de Alianzas y Conflictos: Tácticas, Objetivos y Recomendaciones)
Engine de cálculo matemático prospectivo riguroso basado en la metodología de Michel Godet (LIPSOR)
y sus variantes avanzadas (Multi-criterio / SoftProsp, Difusa, Teoría de Juegos y Simulación de Escenarios).
"""

import numpy as np
from typing import List, Dict, Any, Optional

class MactorEngine:
    def __init__(
        self,
        actors: List[Dict[str, Any]],
        objectives: List[Dict[str, Any]],
        mid: List[List[float]],
        mao2: List[List[float]],
        variant: str = "softprosp",  # 'softprosp', 'lipsor_standard', 'fuzzy', 'game_theory'
        options: Optional[Dict[str, Any]] = None
    ):
        self.actors = actors
        self.objectives = objectives
        self.N = len(actors)
        self.M = len(objectives)
        self.variant = variant
        self.options = options or {}
        
        # Parse and sanitize matrices
        self.mid = np.array(mid, dtype=float)
        if self.mid.shape != (self.N, self.N):
            raise ValueError(f"MID shape must be ({self.N}, {self.N}), got {self.mid.shape}")
            
        self.mao2 = np.array(mao2, dtype=float)
        if self.mao2.shape != (self.N, self.M):
            raise ValueError(f"2MAO shape must be ({self.N}, {self.M}), got {self.mao2.shape}")

        # Weights of objectives (defaults to uniform or custom weight)
        weights = [float(o.get('weight', 1.0)) for o in objectives]
        total_w = sum(weights)
        if total_w <= 0:
            weights = [1.0 / self.M] * self.M
        else:
            weights = [w / total_w for w in weights]
        self.weights = np.array(weights)

    def calculate_mid_metrics(self) -> Dict[str, Any]:
        """Calculates Direct Influences (I_i) and Direct Dependences (D_i)."""
        # Set diagonal to zero for influence calculation if not already
        mid_diag_zero = self.mid.copy()
        np.fill_diagonal(mid_diag_zero, 0)
        
        influence_direct = np.sum(mid_diag_zero, axis=1) # Row sum
        dependence_direct = np.sum(mid_diag_zero, axis=0) # Col sum
        
        return {
            "influence": influence_direct.tolist(),
            "dependence": dependence_direct.tolist(),
            "total_influence": float(np.sum(influence_direct))
        }

    def calculate_midi(self) -> np.ndarray:
        """
        Calculates Matrix of Direct and Indirect Influences (MIDI).
        Includes 2nd order influences through relay actors.
        MIDI_ij = MID_ij + sum_k (MID_ik * MID_kj / Norm)
        """
        mid_diag_zero = self.mid.copy()
        np.fill_diagonal(mid_diag_zero, 0)
        
        # Second order influences: matrix multiplication
        mid_sq = np.dot(mid_diag_zero, mid_diag_zero)
        max_possible = max(1.0, float(np.max(mid_diag_zero)) * self.N)
        
        # Normalized second order contribution
        midi = mid_diag_zero + (mid_sq / max_possible)
        np.fill_diagonal(midi, 0)
        return midi

    def calculate_force_ratios(self, midi: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """
        Calculates Force Ratios (r_i) as formulated by Michel Godet (LIPSOR).
        r_i = [ (I_i - D_i) or (I_i / (I_i + D_i)) * (I_i / Sum(I)) ] normalized.
        """
        if midi is None:
            midi = self.calculate_midi()
            
        I_star = np.sum(midi, axis=1) # Indirect influence
        D_star = np.sum(midi, axis=0) # Indirect dependence
        
        sum_I_star = np.sum(I_star)
        if sum_I_star == 0:
            sum_I_star = 1.0
            
        R_i = np.zeros(self.N)
        for i in range(self.N):
            denom = I_star[i] + D_star[i]
            if denom == 0:
                R_i[i] = 1.0 / self.N
            else:
                # Godet standard power indicator
                R_i[i] = (I_star[i] / sum_I_star) * (I_star[i] / denom)
                
        sum_R = np.sum(R_i)
        if sum_R == 0:
            r_norm = np.ones(self.N)
        else:
            # Normalized so that average is 1.0 (Godet standard)
            r_norm = (R_i / sum_R) * self.N
            
        return {
            "I_star": I_star.tolist(),
            "D_star": D_star.tolist(),
            "R_raw": R_i.tolist(),
            "r_i": r_norm.tolist(),
            "r_normalized_sum1": (R_i / (sum_R if sum_R > 0 else 1.0)).tolist()
        }

    def calculate_1mao(self) -> np.ndarray:
        """
        Calculates 1MAO matrix (signs):
        +1: In favor
        -1: Opposed
         0: Neutral / indifferent
        """
        sign_matrix = np.zeros_like(self.mao2)
        sign_matrix[self.mao2 > 0] = 1
        sign_matrix[self.mao2 < 0] = -1
        return sign_matrix

    def calculate_3mao(self, r_i: np.ndarray) -> np.ndarray:
        """
        Calculates 3MAO matrix (Valuated and Weighted Positions).
        3MAO_ij = r_i * 2MAO_ij (or weighted with objective weights in SoftProsp variant)
        """
        mao3 = np.zeros((self.N, self.M))
        for i in range(self.N):
            for j in range(self.M):
                if self.variant == "softprosp":
                    # SoftProsp weighted objective formula
                    mao3[i, j] = self.mao2[i, j] * self.weights[j] * r_i[i]
                else:
                    # LIPSOR pure formula
                    mao3[i, j] = self.mao2[i, j] * r_i[i]
        return mao3

    def calculate_caa(self, mao1: np.ndarray, r_i: np.ndarray) -> Dict[str, Any]:
        """
        Calculates Convergence Matrices:
        - 1CAA: Simple convergence (shared objective signs)
        - 2CAA: Valuated convergence (minimum or mutual intensity)
        - 3CAA: Weighted valuated convergence (incorporating force ratios r_i and objective weights)
        """
        caa1 = np.zeros((self.N, self.N))
        caa2 = np.zeros((self.N, self.N))
        caa3 = np.zeros((self.N, self.N))

        for i in range(self.N):
            for k in range(self.N):
                if i == k:
                    continue
                sum_1 = 0.0
                sum_2 = 0.0
                sum_3 = 0.0
                for j in range(self.M):
                    # Convergence occurs when both actors agree: both positive or both negative
                    s_i = mao1[i, j]
                    s_k = mao1[k, j]
                    if s_i != 0 and s_k != 0 and (s_i * s_k > 0):
                        # Both in favor or both against
                        sum_1 += 1.0
                        val_min = min(abs(self.mao2[i, j]), abs(self.mao2[k, j]))
                        sum_2 += val_min
                        
                        if self.variant == "softprosp":
                            # SoftProsp weighting with objective weight
                            w_j = self.weights[j]
                            intensity = val_min * w_j
                            power_factor = (r_i[i] + r_i[k]) / 2.0
                            sum_3 += intensity * power_factor * 4.0 # Scale factor consistent with SoftProsp
                        else:
                            # Standard Godet 3CAA
                            sum_3 += 0.5 * (r_i[i] * abs(self.mao2[i, j]) + r_i[k] * abs(self.mao2[k, j]))
                caa1[i, k] = sum_1
                caa2[i, k] = sum_2
                caa3[i, k] = round(sum_3, 2)

        actor_convergence = np.sum(caa3, axis=1)

        return {
            "caa1": caa1.tolist(),
            "caa2": caa2.tolist(),
            "caa3": caa3.tolist(),
            "actor_convergence": actor_convergence.tolist()
        }

    def calculate_daa(self, mao1: np.ndarray, r_i: np.ndarray) -> Dict[str, Any]:
        """
        Calculates Divergence Matrices (Conflicts):
        - 1DAA: Simple divergence (opposing signs)
        - 2DAA: Valuated divergence
        - 3DAA: Weighted valuated divergence
        """
        daa1 = np.zeros((self.N, self.N))
        daa2 = np.zeros((self.N, self.N))
        daa3 = np.zeros((self.N, self.N))

        for i in range(self.N):
            for k in range(self.N):
                if i == k:
                    continue
                sum_1 = 0.0
                sum_2 = 0.0
                sum_3 = 0.0
                for j in range(self.M):
                    s_i = mao1[i, j]
                    s_k = mao1[k, j]
                    # Divergence occurs when one is in favor (+1) and the other opposed (-1)
                    if s_i != 0 and s_k != 0 and (s_i * s_k < 0):
                        sum_1 += 1.0
                        val_min = min(abs(self.mao2[i, j]), abs(self.mao2[k, j]))
                        sum_2 += val_min
                        
                        if self.variant == "softprosp":
                            w_j = self.weights[j]
                            intensity = val_min * w_j
                            power_factor = (r_i[i] + r_i[k]) / 2.0
                            sum_3 += intensity * power_factor * 4.0
                        else:
                            sum_3 += 0.5 * (r_i[i] * abs(self.mao2[i, j]) + r_i[k] * abs(self.mao2[k, j]))
                daa1[i, k] = sum_1
                daa2[i, k] = sum_2
                daa3[i, k] = round(sum_3, 2)

        actor_divergence = np.sum(daa3, axis=1)

        return {
            "daa1": daa1.tolist(),
            "daa2": daa2.tolist(),
            "daa3": daa3.tolist(),
            "actor_divergence": actor_divergence.tolist()
        }

    def calculate_coo(self, mao1: np.ndarray, mao3: np.ndarray) -> Dict[str, Any]:
        """
        Calculates Objective Distances / Mobilization (2COO, 3COO):
        Degrees to which objectives share supporting or opposing actors.
        """
        coo2 = np.zeros((self.M, self.M))
        coo3 = np.zeros((self.M, self.M))

        for j in range(self.M):
            for l in range(self.M):
                if j == l:
                    continue
                sum_2 = 0.0
                sum_3 = 0.0
                for i in range(self.N):
                    if mao1[i, j] != 0 and mao1[i, l] != 0 and (mao1[i, j] * mao1[i, l] > 0):
                        sum_2 += min(abs(self.mao2[i, j]), abs(self.mao2[i, l]))
                        sum_3 += 0.5 * (abs(mao3[i, j]) + abs(mao3[i, l]))
                coo2[j, l] = sum_2
                coo3[j, l] = round(sum_3, 2)

        return {
            "coo2": coo2.tolist(),
            "coo3": coo3.tolist()
        }

    def calculate_objective_metrics(self, mao1: np.ndarray, mao3: np.ndarray) -> List[Dict[str, Any]]:
        """
        Computes mobilization, consensus, and conflict index for each objective.
        """
        metrics = []
        for j in range(self.M):
            favorable_count = int(np.sum(mao1[:, j] > 0))
            opposed_count = int(np.sum(mao1[:, j] < 0))
            neutral_count = int(np.sum(mao1[:, j] == 0))
            
            # Mobilization: total weighted intensity focused on this objective
            mobilization = float(np.sum(np.abs(mao3[:, j])))
            # Net Balance: favorable weighted minus opposed weighted
            balance = float(np.sum(mao3[:, j]))
            
            # Conflict degree: high when both favorable and opposed have high weights
            fav_power = float(np.sum(np.maximum(0, mao3[:, j])))
            opp_power = float(np.sum(np.maximum(0, -mao3[:, j])))
            conflict_index = round(2.0 * min(fav_power, opp_power) / (fav_power + opp_power + 1e-6), 3)

            metrics.append({
                "index": j,
                "id": self.objectives[j].get("id", f"O{j+1}"),
                "name": self.objectives[j].get("name", f"Objetivo {j+1}"),
                "weight": float(self.weights[j]),
                "favorable_actors": favorable_count,
                "opposed_actors": opposed_count,
                "neutral_actors": neutral_count,
                "mobilization": round(mobilization, 2),
                "net_balance": round(balance, 2),
                "conflict_index": conflict_index,
                "status": "Consensuado" if conflict_index < 0.25 and favorable_count > opposed_count else (
                    "En Disputa Crítica" if conflict_index > 0.6 else "Moderado / Negociable"
                )
            })
        return metrics

    def classify_actors_quadrant(self, influence: List[float], dependence: List[float]) -> List[Dict[str, Any]]:
        """
        Classifies actors into Godet's 4 strategic quadrants:
        - Dominant (Alto influjo, baja dependencia)
        - Liaison / Relay (Alto influjo, alta dependencia)
        - Autonomous (Bajo influjo, baja dependencia)
        - Dependent (Bajo influjo, alta dependencia)
        """
        mean_inf = np.mean(influence)
        mean_dep = np.mean(dependence)

        classification = []
        for i in range(self.N):
            inf = influence[i]
            dep = dependence[i]
            if inf >= mean_inf and dep < mean_dep:
                quadrant = "Dominante (Actor Clave)"
                color = "#3b82f6" # Blue
                description = "Capacidad alta de imponer su agenda sin depender críticamente de los demás."
            elif inf >= mean_inf and dep >= mean_dep:
                quadrant = "Enlace / Relé (Actor Pivote)"
                color = "#f59e0b" # Orange
                description = "Altamente inestable y reactivo; sus movimientos conmocionan todo el sistema."
            elif inf < mean_inf and dep >= mean_dep:
                quadrant = "Dependiente (Actor Vulnerable)"
                color = "#ef4444" # Red
                description = "Receptor pasivo de las decisiones de los actores dominantes y enlaces."
            else:
                quadrant = "Autónomo (Actor de Margen)"
                color = "#10b981" # Green
                description = "Poca vinculación directa; sus objetivos operan en nichos independientes."

            classification.append({
                "index": i,
                "id": self.actors[i].get("id", f"A{i+1}"),
                "name": self.actors[i].get("name", f"Actor {i+1}"),
                "influence": round(inf, 2),
                "dependence": round(dep, 2),
                "quadrant": quadrant,
                "color": color,
                "description": description
            })
        return classification

    def compute_coalition_stability(self, caa3: np.ndarray, daa3: np.ndarray, r_i: np.ndarray) -> Dict[str, Any]:
        """
        Game-Theoretic Coalitional Stability Variant:
        Determines core coalitions and assesses whether an alliance is robust
        against defection or counter-coalitions.
        """
        coalitions = []
        # Find dominant alliance pairs (high convergence, zero or minimal divergence)
        for i in range(self.N):
            for k in range(i + 1, self.N):
                c_val = caa3[i, k]
                d_val = daa3[i, k]
                if c_val > 0 or d_val > 0:
                    net_affinity = c_val - d_val
                    stability = "Muy Estable" if d_val == 0 and c_val > 5 else (
                        "Alianza Táctica" if net_affinity > 0 else (
                            "Conflicto Severo" if net_affinity < -5 else "Tensión Latente"
                        )
                    )
                    coalitions.append({
                        "actor1": self.actors[i].get("name", f"A{i+1}"),
                        "actor2": self.actors[k].get("name", f"A{k+1}"),
                        "convergence": round(float(c_val), 2),
                        "divergence": round(float(d_val), 2),
                        "net_affinity": round(float(net_affinity), 2),
                        "stability": stability
                    })
        # Sort by net affinity descending
        coalitions.sort(key=lambda x: x["net_affinity"], reverse=True)
        return {"coalitions": coalitions}

    def compute_hierarchical_dendrogram(self, matrix: np.ndarray, is_convergence: bool = True) -> Dict[str, Any]:
        """
        Computes Hierarchical Clustering (Árbol de Convergencia / Divergencia de Michel Godet - LIPSOR).
        Uses average-linkage (UPGMA) over distances derived from the 3CAA or 3DAA matrix.
        Returns a tree structure with heights, cluster leaves, and coalitional blocks.
        """
        N = self.N
        if N < 2:
            return {"tree": None, "leaves": []}

        max_val = float(np.max(matrix))
        if max_val == 0:
            max_val = 1.0

        # Construct distance matrix
        dist = np.zeros((N, N))
        for i in range(N):
            for j in range(N):
                if i != j:
                    if is_convergence:
                        # Higher convergence => smaller distance
                        dist[i, j] = max(0.0, max_val - matrix[i, j])
                    else:
                        # Higher divergence => smaller distance in conflict tree
                        dist[i, j] = max(0.0, max_val - matrix[i, j])

        clusters = []
        for i in range(N):
            act = self.actors[i]
            clusters.append({
                "id": i,
                "label": act.get("short_name", act.get("name", f"A{i+1}")),
                "full_name": act.get("name", f"A{i+1}"),
                "height": 0.0,
                "elements": [i],
                "left": None,
                "right": None,
                "is_leaf": True
            })

        step = 0
        while len(clusters) > 1:
            k = len(clusters)
            min_d = float('inf')
            best_pair = (0, 1)

            for i in range(k):
                for j in range(i + 1, k):
                    elems_i = clusters[i]["elements"]
                    elems_j = clusters[j]["elements"]
                    avg_d = sum(dist[ei, ej] for ei in elems_i for ej in elems_j) / (len(elems_i) * len(elems_j))
                    if avg_d < min_d:
                        min_d = avg_d
                        best_pair = (i, j)

            i, j = best_pair
            c1 = clusters[i]
            c2 = clusters[j]

            merged = {
                "id": N + step,
                "label": f"Bloque ({c1['label']} + {c2['label']})",
                "height": round(float(min_d), 2),
                "similarity": round(float(max_val - min_d), 2),
                "elements": c1["elements"] + c2["elements"],
                "left": c1,
                "right": c2,
                "is_leaf": False
            }
            step += 1
            clusters = [c for idx, c in enumerate(clusters) if idx not in (i, j)]
            clusters.append(merged)

        root = clusters[0] if clusters else None

        # Extract ordered leaves from tree
        leaves = []
        def traverse(node):
            if not node:
                return
            if node.get("is_leaf"):
                leaves.append({
                    "id": node["id"],
                    "label": node["label"],
                    "full_name": node["full_name"]
                })
            else:
                traverse(node.get("left"))
                traverse(node.get("right"))
        traverse(root)

        return {
            "root": root,
            "leaves": leaves,
            "max_distance": round(max_val, 2)
        }

    def calculate_network_centrality(self) -> Dict[str, Any]:
        """
        Calcula indicadores topológicos de Análisis de Redes Sociales (SNA)
        sobre la Matriz de Influencia Directa (MID):
          1. Centralidad de Grado de Salida (Out-Degree / Motricidad normalizada): C_out(i)
          2. Centralidad de Grado de Entrada (In-Degree / Dependencia normalizada): C_in(i)
          3. Índice de Centralización de la Red (Freeman Centralization Index) para salida y entrada.
          4. Densidad de la Red (Density).
        """
        mid_diag_zero = self.mid.copy()
        np.fill_diagonal(mid_diag_zero, 0)
        
        N = self.N
        max_possible_per_node = max(1.0, 4.0 * (N - 1)) # Máximo flujo que un nodo puede emitir/recibir (escala 0-4)
        
        # Grados ponderados
        out_degree = np.sum(mid_diag_zero, axis=1) # Influencia que emite
        in_degree = np.sum(mid_diag_zero, axis=0)  # Dependencia que absorbe
        
        # Centralidades normalizadas de 0 a 1 (o 0% a 100%)
        out_centrality = out_degree / max_possible_per_node
        in_centrality = in_degree / max_possible_per_node
        
        # Índice de Centralización de Freeman:
        # C_net = sum(max(C) - C(i)) / [ (N - 2) * max_possible ] o normalizado sobre la red estrella
        max_out = np.max(out_degree)
        max_in = np.max(in_degree)
        
        # Denominador teórico máximo para grafo dirigido ponderado estrella
        denom_freeman = (N - 1) * max_possible_per_node if N > 1 else 1.0
        
        centralization_out = float(np.sum(max_out - out_degree) / denom_freeman) if denom_freeman > 0 else 0.0
        centralization_in = float(np.sum(max_in - in_degree) / denom_freeman) if denom_freeman > 0 else 0.0
        
        # Densidad de red (proporción de relaciones activas > 0)
        total_possible_edges = N * (N - 1) if N > 1 else 1
        active_edges = int(np.count_nonzero(mid_diag_zero))
        density = float(active_edges / total_possible_edges) if total_possible_edges > 0 else 0.0
        
        # Intensidad media de la red
        mean_intensity = float(np.sum(mid_diag_zero) / total_possible_edges) if total_possible_edges > 0 else 0.0

        return {
            "out_centrality": [round(float(x), 3) for x in out_centrality],
            "in_centrality": [round(float(x), 3) for x in in_centrality],
            "centralization_out": round(max(0.0, min(1.0, centralization_out)), 3),
            "centralization_in": round(max(0.0, min(1.0, centralization_in)), 3),
            "density": round(density, 3),
            "mean_intensity": round(mean_intensity, 2),
            "active_edges": active_edges,
            "total_possible_edges": total_possible_edges
        }

    def run_all(self) -> Dict[str, Any]:
        """Runs the complete MACTOR workflow and returns comprehensive prospective results."""
        # Step 1: Direct Influence / Dependence
        mid_metrics = self.calculate_mid_metrics()
        network_metrics = self.calculate_network_centrality()
        
        # Step 2: MIDI & Force Ratios (r_i)
        midi = self.calculate_midi()
        force_metrics = self.calculate_force_ratios(midi)
        r_i = np.array(force_metrics["r_i"])
        
        # Step 3: Positions 1MAO, 2MAO, 3MAO
        mao1 = self.calculate_1mao()
        mao3 = self.calculate_3mao(r_i)
        
        # Step 4: Convergences (1CAA, 2CAA, 3CAA)
        caa_results = self.calculate_caa(mao1, r_i)
        
        # Step 5: Divergences (1DAA, 2DAA, 3DAA)
        daa_results = self.calculate_daa(mao1, r_i)
        
        # Step 6: Objectives Distance (2COO, 3COO) and mobilization
        coo_results = self.calculate_coo(mao1, mao3)
        obj_metrics = self.calculate_objective_metrics(mao1, mao3)
        
        # Step 7: Quadrant Classification
        quadrants = self.classify_actors_quadrant(mid_metrics["influence"], mid_metrics["dependence"])
        
        # Step 8: Game-Theoretic Coalition Stability
        coalitions = self.compute_coalition_stability(
            np.array(caa_results["caa3"]),
            np.array(daa_results["daa3"]),
            r_i
        )
        
        # Step 9: Hierarchical Convergence and Divergence Trees (Michel Godet Dendrograms)
        caa3_np = np.array(caa_results["caa3"])
        daa3_np = np.array(daa_results["daa3"])
        convergence_tree = self.compute_hierarchical_dendrogram(caa3_np, is_convergence=True)
        divergence_tree = self.compute_hierarchical_dendrogram(daa3_np, is_convergence=False)

        # Determine dominant actor / winner according to MACTOR convergence sum
        conv_sums = caa_results["actor_convergence"]
        best_actor_idx = int(np.argmax(conv_sums))
        best_actor = self.actors[best_actor_idx]
        
        return {
            "variant": self.variant,
            "actors": self.actors,
            "objectives": self.objectives,
            "weights": self.weights.tolist(),
            "mid": self.mid.tolist(),
            "midi": np.round(midi, 2).tolist(),
            "mid_metrics": mid_metrics,
            "network_metrics": network_metrics,
            "force_metrics": force_metrics,
            "mao1": mao1.tolist(),
            "mao2": self.mao2.tolist(),
            "mao3": np.round(mao3, 2).tolist(),
            "caa1": caa_results["caa1"],
            "caa2": caa_results["caa2"],
            "caa3": caa_results["caa3"],
            "actor_convergence": caa_results["actor_convergence"],
            "daa1": daa_results["daa1"],
            "daa2": daa_results["daa2"],
            "daa3": daa_results["daa3"],
            "actor_divergence": daa_results["actor_divergence"],
            "coo2": coo_results["coo2"],
            "coo3": coo_results["coo3"],
            "objective_metrics": obj_metrics,
            "quadrants": quadrants,
            "coalitions": coalitions["coalitions"],
            "convergence_tree": convergence_tree,
            "divergence_tree": divergence_tree,
            "dominant_actor": {
                "index": best_actor_idx,
                "name": best_actor.get("name", f"Actor {best_actor_idx+1}"),
                "convergence_score": round(conv_sums[best_actor_idx], 2),
                "r_i": round(r_i[best_actor_idx], 2)
            }
        }
