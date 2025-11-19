import os
import random
import math
import time
import numpy as np
import statistics
import pandas as pd

import sys
# ensure project root is on path so we can import sibling modules (cv4, cv5, ...)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import base.functions as functions
import cv4.cv4 as de_module
import cv5.cv5 as pso_module
import cv6.cv6 as soma_module
import cv8.cv8 as fa_module


def clip_vec(x, lb, ub):
	return np.minimum(np.maximum(x, lb), ub)

def tlbo(func, D, NP, max_ofe, lb=None, ub=None):
	if lb is None or ub is None:
		lb, ub = func.bounds
	lb = np.array([lb] * D)
	ub = np.array([ub] * D)

	pop = np.random.uniform(lb, ub, (NP, D))
	fitness = np.array([func.do(ind.tolist()) for ind in pop])
	ofe = NP

	max_gen = max(0, (max_ofe - ofe) // NP)

	for gen in range(int(max_gen)):
		teacher_idx = int(np.argmin(fitness))
		teacher = pop[teacher_idx]
		mean = np.mean(pop, axis=0)
		T = 1 if random.random() < 0.5 else 2
		for i in range(NP):
			new = pop[i] + np.random.rand(D) * (teacher - T * mean)
			new = clip_vec(new, lb, ub)
			f = func.do(new.tolist())
			ofe += 1
			if f < fitness[i]:
				pop[i] = new
				fitness[i] = f
			if ofe >= max_ofe:
				break
		if ofe >= max_ofe:
			break

		for _ in range(NP):
			i, j = np.random.choice(NP, 2, replace=False)
			if fitness[i] < fitness[j]:
				new = pop[j] + np.random.rand(D) * (pop[i] - pop[j])
				new = clip_vec(new, lb, ub)
				f = func.do(new.tolist())
				ofe += 1
				if f < fitness[j]:
					pop[j] = new
					fitness[j] = f
			else:
				new = pop[i] + np.random.rand(D) * (pop[j] - pop[i])
				new = clip_vec(new, lb, ub)
				f = func.do(new.tolist())
				ofe += 1
				if f < fitness[i]:
					pop[i] = new
					fitness[i] = f
			if ofe >= max_ofe:
				break
		if ofe >= max_ofe:
			break

	return float(np.min(fitness))


def run_experiments(function_names=None, D=30, NP=30, Max_OFE=3000, experiments=30):
	if function_names is None:
		function_names = list(functions.function_dict.keys())

	algs = {
		"TLBO": tlbo,
		"DE": lambda f, D, NP, Max_OFE, lb, ub: (
			de_module.shade(f.func if hasattr(f, 'func') else f, pop_size=NP, dim=D, max_gen=max(1, Max_OFE//NP), lb=lb, ub=ub)[1][2]
		),
		"PSO": lambda f, D, NP, Max_OFE, lb, ub: (
			pso_module.particle_swarm_optimization(func=f, dim=D, num_particles=NP, max_iter=max(1, Max_OFE//NP))[1][1]
		),
		"SOMA": lambda f, D, NP, Max_OFE, lb, ub: (
			soma_module.soma(func=f, pop_size=NP, dim=D, migrations=max(1, Max_OFE//NP))[1][1]
		),
		"FA": lambda f, D, NP, Max_OFE, lb, ub: (
			fa_module.firefly_algorithm(func=f, dim=D, n_fireflies=NP, max_iter=max(1, Max_OFE//NP))[1][1]
		),
	}

	raw_rows = []
	summary_rows = []

	for fname in function_names:
		func_obj = functions.function_dict[fname]
		lb, ub = func_obj.bounds
		print(f"Running function: {fname}")
		for alg_name, alg_func in algs.items():
			print(f"Running algorithm: {alg_name} for {fname}")
			results = []
			for exp in range(experiments):
				# set seed for reproducibility per experiment
				random.seed(exp + 1234)
				np.random.seed(exp + 1234)
				best = alg_func(func_obj, D, NP, Max_OFE, lb=lb, ub=ub)
				results.append(best)
				raw_rows.append({"Function": fname, "Algorithm": alg_name, "Experiment": exp + 1, "Best": best})
			mean_v = statistics.mean(results)
			std_v = statistics.pstdev(results)
			summary_rows.append({"Function": fname, "Algorithm": alg_name, "Mean": mean_v, "StdDev": std_v})
			print(f"{alg_name}: mean={mean_v:.6e}, std={std_v:.6e}")

	timestamp = int(time.time())
	out_dir = os.path.dirname(__file__)
	raw_file = os.path.join(out_dir, f"results_raw_{timestamp}.csv")
	import csv
	with open(raw_file, "w", newline="") as f:
		writer = csv.DictWriter(f, fieldnames=["Function", "Algorithm", "Experiment", "Best"])
		writer.writeheader()
		for r in raw_rows:
			writer.writerow(r)

	summary_file = os.path.join(out_dir, f"results_summary_{timestamp}.csv")
	with open(summary_file, "w", newline="") as f:
		writer = csv.DictWriter(f, fieldnames=["Function", "Algorithm", "Mean", "StdDev"])
		writer.writeheader()
		for r in summary_rows:
			writer.writerow(r)

	# create an Excel file with a summary, raw data and per-function sheets
	df_raw = pd.DataFrame(raw_rows)
	df_summary = pd.DataFrame(summary_rows)
	xlsx_file = os.path.join(out_dir, f"results_{timestamp}.xlsx")
	# desired column order in per-function tables
	alg_order = ["DE", "PSO", "SOMA", "FA", "TLBO"]
	with pd.ExcelWriter(xlsx_file, engine="openpyxl") as writer:
		# write summary and raw sheets
		df_summary.to_excel(writer, sheet_name="summary", index=False)
		df_raw.to_excel(writer, sheet_name="raw", index=False)
		# create per-function sheets formatted like the provided table
		for fname in function_names:
			# build empty table for experiments
			index = [f"Experiment {i}" for i in range(1, experiments + 1)]
			df_table = pd.DataFrame(index=index, columns=alg_order)
			# fill values from raw_rows
			for r in raw_rows:
				if r["Function"] != fname:
					continue
				alg = r["Algorithm"]
				exp = int(r["Experiment"])
				if alg in alg_order and 1 <= exp <= experiments:
					df_table.at[f"Experiment {exp}", alg] = r["Best"]
			# compute mean/std and append as last row
			mean_std_row = []
			for alg in alg_order:
				vals = df_table[alg].dropna().astype(float).tolist()
				if len(vals) > 0:
					mean_v = statistics.mean(vals)
					std_v = statistics.pstdev(vals)
					mean_std_row.append(f"{mean_v:.6e} / {std_v:.6e}")
				else:
					mean_std_row.append("")
			df_table.loc[f"Mean/Std dev"] = mean_std_row
			# write sheet (sheet name must be <=31 chars)
			safe_name = str(fname)[:31]
			df_table.to_excel(writer, sheet_name=safe_name)
	print(f"Wrote Excel results to {xlsx_file}")



if __name__ == "__main__":
	D = 10
	NP = 30
	Max_OFE = 3000
	experiments = 30

	# restrict functions to a reasonable subset (all defined functions)
	function_names = list(functions.function_dict.keys())

	run_experiments(function_names=function_names, D=D, NP=NP, Max_OFE=Max_OFE, experiments=experiments)

