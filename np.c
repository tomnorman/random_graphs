#include <math.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>

typedef unsigned int uint;

// fills 'ps' with the powerset of binary('counter'), 'i' indicates where to finish
uint powerset(uint nodes, uint counter, uint* ps) {
	// https://www.geeksforgeeks.org/power-set/

	int i = 0;
	for (uint j = 0; j < nodes; j++)
		if (counter & (1 << j)) // 'j' in binary('counter')
			ps[i++] = j;
	
	return i;
}

bool maximal(double* mat, uint nodes, uint s, uint* ps, char t) {
	for (uint i = 0; i < s; i++) { //rows
		for (uint j = 0; j < s; j++) { //columns
			if (i <= j) continue; // mat is symmetric & digonal isn't edges
			double edge = mat[nodes * ps[i] + ps[j]];
			bool independent = (t == 'i' && edge == 0);
			bool clique = (t == 'c' && edge != 0);
			if ((independent || clique) == false)
			       	return false;
		}
	}

	return true;
}

double* subMat(double* mat, uint nodes, uint* S, uint nodes_S) {
	double* sub = (double*)malloc(nodes_S * nodes_S * sizeof(double));

	for (uint i = 0; i < nodes_S; i++) { //rows
		for (uint j = 0; j < nodes_S; j++) { //columns
			if (i <= j) continue; // mat is symmetric & digonal isn't edges
			sub[nodes_S * i + j] = mat[nodes * S[i] + S[j]];
		}
	}

	return sub;
}

uint maxes(double* mat, uint nodes, char t) {
	uint n = pow(2, nodes);
	uint* ps = (uint*)malloc(nodes * sizeof(uint));
	uint max_counter = 0; //convert to binary to get the max powerset
	uint max_s = 0;


	for (uint counter = 1; counter < n; counter++) {
		uint s = powerset(nodes, counter, ps);

		bool flag = maximal(mat, nodes, s, ps, t);
		if (flag == true && max_s < s) {
			max_s = s;
			max_counter = counter;
		}
	}

	free(ps);

	return max_counter;
}

uint chi(double* mat, uint nodes, float a) {
	uint k = nodes;
	uint* S = (uint*)malloc(nodes * sizeof(uint));
	uint* not_S = (uint*)malloc(nodes * sizeof(uint));

	uint tmp;
	for (uint counter = 1; counter < nodes; counter++) {
		uint nodes_S = powerset(nodes, counter, S);
		uint nodes_not_S = powerset(nodes, ~counter, not_S);

		double* mat_not_S = subMat(mat, nodes, not_S, nodes_not_S);
		
		if ((maximal(mat, nodes, nodes_S, S, 'i')) && (nodes_S >= a * nodes)) {
			tmp = chi(mat_not_S, nodes_not_S, a);
			if (k > 1 + tmp)	k = 1 + tmp;
		}

		if (((nodes - a * nodes) / 2 <= nodes_S) && (nodes_S <= nodes / 2)) {
			double* mat_S = subMat(mat, nodes, S, nodes_S);
			tmp = chi(mat_S, nodes_S, a) + chi(mat_not_S, nodes_S, a);
			if (k > tmp)	k = tmp;
		}

		free(mat_not_S);
	}

	free(S);
	free(not_S);

	return k;
}
