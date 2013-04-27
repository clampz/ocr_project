"""
  main.py
  by David Weinman
  4/23/13, 3:25a
"""

"""

fully_trained = FALSE
DO UNTIL (fully_trained):
	fully_trained = TRUE
	FOR EACH training_vector = <X1, X2, ..., Xn, theta, target>::
		#Weights compared to theta
		a = (X1 * W1) + (X2 * W2) + ... + (Xn * Wn) - theta
		y = sigma(a)
		IF y != target:
			fully_trained = FALSE
		FOR EACH Wi:
		MODIFY_WEIGHT(Wi)
	IF (fully_trained):
		BREAK

"""


def main():
	inputObj = backPropFieldObj()
	max_iterations = inputObj.n_max_iterations
	error_threshhold = inputObj.n_error_threshhold
	

if __name__ == "__main__": main()

