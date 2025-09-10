from fitted_params import *

def get_m_c(algo, refdb):
	assert refdb == "scop40" or refdb == "scop40c"
	m, c = algo_refdb2m_c[(algo, refdb)]
	return m, c

def estimate_C(score, m, c):
	logC = -(m*score + c)
	C = min(10**logC, 1)
	return C

def estimate_h(algo, q, db):
	if algo == "tm":
		return 1
	elif algo == "dali":
		return 0.04
	elif algo == "foldseek":
		return 0.04
	elif algo == "reseek":
		return 0.005
	assert False

def estimate_PF(algo):
	if algo == "tm":
		return 1
	elif algo == "dali":
		return 0.5
	elif algo == "foldseek":
		return 1
	elif algo == "reseek":
		return 1
	assert False

def estimate_FPEPQ(algo, refdb, score, dbsize, PF, h):
	m, c = get_m_c(algo, refdb)
	C = estimate_C(score, m, c)
	return C*dbsize*h*PF
