#include "lowWaterEquations.h"
#include <iostream>
#include <vector>



lowWaterEquations::lowWaterEquations(float nalpha, float nbeta, float ng, float nr, float nstart, float nend, float ntime, int n)
{
	alpha = nalpha;
	beta = nbeta;
	g = ng;
	r = nr;
	start = nstart;
	end = nend;
	time = ntime;
	N = n + 1; //количество точек
	deltax = (end - start) / (float)n;


	i_points = std::vector<float>(2 * N - 1);
	h1 = std::vector<float>(2 * N - 1);
	h2 = std::vector<float>(2 * N - 1);
	u1 = std::vector<float>(2 * N - 1);
	u2 = std::vector<float>(2 * N - 1);
	b_points = std::vector<float>(2 * N - 1);


	omega1 = std::vector<float>(2 * N - 1);
	omega2 = std::vector<float>(2 * N - 1);
	c1 = std::vector<float>(2 * N - 1);
	c2 = std::vector<float>(2 * N - 1);
	tau1 = std::vector<float>(2 * N - 1);
	tau2 = std::vector<float>(2 * N - 1);
	P1 = std::vector<float>(2 * N - 1);
	P2 = std::vector<float>(2 * N - 1);
	j1 = std::vector<float>(2 * N - 1);
	j2 = std::vector<float>(2 * N - 1);

	for (int i = 0; i < 2 * N - 1; i += 2) {
		float tmp = (nend - nstart) / (2 * N - 2) * i + nstart;
		i_points[i] = tmp;
		b_points[i] = b(tmp);
		h1[i] = start_h1(tmp);
		h2[i] = start_h2(tmp);
		u1[i] = start_u1(tmp);
		u2[i] = start_u2(tmp);


		if (h1[i] < 0.001) {
			h1[i] = 0;
			c1[i] = 0;
			tau1[i] = 0;
		}
		else {
			c1[i] = sqrt(g * h1[i]);
			tau1[i] = alpha * deltax / sqrt(g * h1[i]);
		}
		if (h2[i] < 0.001) {
			h2[i] = 0;
			tau2[i] = 0;
			c2[i] = 0;
		}

		else {
			c2[i] = sqrt(g * h2[i]);
			tau2[i] = alpha * deltax / sqrt(g * h2[i]);
		}

	}


	for (int i = 1; i < 2 * N - 1; i += 2) {
		i_points[i] = (i_points[i - 1] + i_points[i + 1]) / 2.0f;
		h1[i] = (h1[i - 1] + h1[i + 1]) / 2.0f;
		h2[i] = (h2[i - 1] + h2[i + 1]) / 2.0f;
		u1[i] = (u1[i - 1] + u1[i + 1]) / 2.0f;
		u2[i] = (u2[i - 1] + u2[i + 1]) / 2.0f;
		b_points[i] = (b_points[i - 1] + b_points[i + 1]) / 2;


		if (h1[i] < 0) {
			h1[i] = 0;
		}
		if (h2[i] < 0) {
			h2[i] = 0;
		}

		//c1[i] = sqrt(g * h1[i]);
		//c2[i] = sqrt(g * h2[i]);

		if (h1[i] < 0.001) {
			h1[i] = 0;
			tau1[i] = 0;
			omega1[i] = 0;
			c1[i] = sqrt(g * h1[i]);
		}
		else {
			c1[i] = sqrt(g * h1[i]);
			tau1[i] = alpha * deltax / sqrt(g * h1[i]);
			omega1[i] = (tau1[i] / h1[i]) *
				((pow((h1[i + 1] * u1[i + 1]), 2) - pow((h1[i - 1] * u1[i - 1]), 2)) / deltax +
					g * h1[i] / deltax * (r * h2[i + 1] + h1[i + 1] + b_points[i + 1] - r * h2[i - 1] - h1[i - 1] - b_points[i - 1]));


		}
		if (h2[i] < 0.001) {
			h2[i] = 0;
			tau2[i] = 0;
			omega2[i] = 0;
			c2[i] = 0;
		}

		else {
			c2[i] = sqrt(g * h2[i]);

			tau2[i] = alpha * deltax / sqrt(g * h2[i]);
			omega2[i] = (tau2[i] / h2[i]) *
				((pow((h2[i + 1] * u2[i + 1]), 2) - pow((h2[i - 1] * u2[i - 1]), 2)) / deltax +
					g * h2[i] / deltax * (h2[i + 1] + h1[i + 1] + b_points[i + 1] - h2[i - 1] - h1[i - 1] - b_points[i - 1]));

		}


		P1[i] = tau1[i] * u1[i] * h1[i] * (u1[i] / deltax * (u1[i + 1] - u1[i - 1]) + g / deltax * (h1[i + 1] - h2[i - 1]) +
			r * g / deltax * (h2[i + 1] - h2[i - 1]) + g / deltax * (b_points[i + 1] - b_points[i - 1])) +
			g * tau1[i] * h1[i] * (h1[i] / deltax * (u1[i + 1] - u1[i - 1]) + u1[i] / deltax * (h1[i + 1] - h1[i - 1]));

		P2[i] = tau2[i] * u2[i] * h2[i] * (u2[i] / deltax * (u2[i + 1] - u2[i - 1]) + g / deltax * (h2[i + 1] - h2[i - 1]) +
			g / deltax * (h1[i + 1] - h1[i - 1]) + g / deltax * (b_points[i + 1] - b_points[i - 1])) +
			g * tau2[i] * h2[i] * (h2[i] / deltax * (u2[i + 1] - u2[i - 1]) + u2[i] / deltax * (h2[i + 1] - h2[i - 1]));



		j1[i] = h1[i] * (u1[i] - omega1[i]);
		j2[i] = h2[i] * (u2[i] - omega2[i]);




	}

	std::vector<float> tmp1(2 * N - 1);
	std::vector<float> tmp2(2 * N - 1);
	for (int i = 0; i < 2 * N - 1; i++) {
		tmp1[i] = deltax / c1[i];
		tmp2[i] = deltax / c2[i];
	}

	deltat = beta * std::min((*std::min_element(tmp1.begin(), tmp1.end())), (*std::min_element(tmp2.begin(), tmp2.end())));
	if (deltat <= 0) {
		throw "deltat <=0";
	}
	if (deltax <= 0) {
		throw "deltax <=0";
	}

	new_h1 = std::vector<std::vector<float>>(1, h1);
	new_h2 = std::vector<std::vector<float>>(1, h2);
	new_u1 = std::vector<std::vector<float>>(1, u1);
	new_u2 = std::vector<std::vector<float>>(1, u2);
}

float lowWaterEquations::start_h1(float x) //инициализаци€ стартовой толщины 1 сло€
{
	float t = 0;
	if (x < 0.5)
	{
		return(0.5);
	}
	else
	{
		return(0.45);
	}

	//return(2.0f - b(x));
}

float lowWaterEquations::start_h2(float x) //инициализаци€ стартовой толщины 2 сло€
{
	float t = 0;
	if (x < 0.5)
	{
		return(0.5);
	}
	else
	{
		return(0.55);
	}
	/*return(1 - start_h1(x)- b(x));*/
}

float lowWaterEquations::b(float x)
{
	//функци€ определ€юща€ дно водоема, возвращает значение значени€ дна в точке
	return(0);
}

float lowWaterEquations::start_u1(float x)
{
	// функци€ задает скорость течени€ первого сло€ воды
	return(2.5);
}

float lowWaterEquations::start_u2(float x)
{
	// функци€ задает скорость течени€ второго сло€ воды
	return(2.5);
}

std::vector<std::vector<float>> lowWaterEquations::solver_u_constant()
{
	{
		float k = 0;
		std::vector<std::vector<float>> res;
		std::vector<float> tmp_h1(2 * N - 1);
		std::vector<float> tmp_h2(2 * N - 1);
		std::vector<float> tmp_u1(2 * N - 1);
		std::vector<float> tmp_u2(2 * N - 1);
		while (k * deltat < time) {
			for (int i = 1; i < 2 * N - 1; i += 2) {
				if (h1[i] < 0.001) {
					h1[i] = 0;
					tau1[i] = 0;
					omega1[i] = 0;
				}
				else {

					tau1[i] = alpha * deltax / sqrt(g * h1[i]);
					omega1[i] = (tau1[i] / h1[i]) *
						((pow((h1[i + 1] * u1[i + 1]), 2) - pow((h1[i - 1] * u1[i - 1]), 2)) / deltax +
							g * h1[i] / deltax * (r * h2[i + 1] + h1[i + 1] + b_points[i + 1] - r * h2[i - 1] - h1[i - 1] - b_points[i - 1]));


				}
				if (h2[i] < 0.001) {
					h2[i] = 0;
					tau2[i] = 0;
					omega2[i] = 0;
				}
				else {
					tau2[i] = alpha * deltax / sqrt(g * h2[i]);
					omega2[i] = (tau2[i] / h2[i]) *
						((pow((h2[i + 1] * u2[i + 1]), 2) - pow((h2[i - 1] * u2[i - 1]), 2)) / deltax +
							g * h2[i] / deltax * (h2[i + 1] + h1[i + 1] + b_points[i + 1] - h2[i - 1] - h1[i - 1] - b_points[i - 1]));
				}


				P1[i] = tau1[i] * u1[i] * h1[i] * (u1[i] / deltax * (u1[i + 1] - u1[i - 1]) + g / deltax * (h1[i + 1] - h2[i - 1]) +
					r * g / deltax * (h2[i + 1] - h2[i - 1]) + g / deltax * (b_points[i + 1] - b_points[i - 1])) +
					g * tau1[i] * h1[i] * (h1[i] / deltax * (u1[i + 1] - u1[i - 1]) + u1[i] / deltax * (h1[i + 1] - h1[i - 1]));


				P2[i] = tau2[i] * u2[i] * h2[i] * (u2[i] / deltax * (u2[i + 1] - u2[i - 1]) + g / deltax * (h2[i + 1] - h2[i - 1]) +
					g / deltax * (h1[i + 1] - h1[i - 1]) + g / deltax * (b_points[i + 1] - b_points[i - 1])) +
					g * tau2[i] * h2[i] * (h2[i] / deltax * (u2[i + 1] - u2[i - 1]) + u2[i] / deltax * (h2[i + 1] - h2[i - 1]));

				j1[i] = h1[i] * (u1[i] - omega1[i]);
				j2[i] = h2[i] * (u2[i] - omega2[i]);
			}

			for (int i = 0; i < 2 * N - 1; i += 2) {

				if (h1[i] < 0.001) {
					h1[i] = 0;
					tau1[i] = 0;
				}
				else {
					tau1[i] = alpha * deltax / sqrt(g * h1[i]);
				}
				if (h2[i] < 0.001) {
					h2[i] = 0;
					tau2[i] = 0;
				}

				else {
					tau2[i] = alpha * deltax / sqrt(g * h2[i]);
				}


				if (i == (2 * N - 2) || i == 0) {
					tmp_h1[i] = h1[i];
					tmp_h2[i] = h2[i];
				}
				else {
					tmp_h1[i] = -(j1[i + 1] - j1[i - 1]) / deltax * deltat + h1[i];

					tmp_h2[i] = -(j2[i + 1] - j2[i - 1]) / deltax * deltat + h2[i];
				}

				if (tmp_h1[i] < 0.001) {
					tmp_h1[i] = 0;
				}
				if (tmp_h2[i] < 0.001) {
					tmp_h2[i] = 0;
				}
				if (tmp_h1[i] != tmp_h1[i]) {
					k = k + 1 - 1;
					throw "fire";

				}
				if (tmp_h2[i] != tmp_h2[i]) {
					k = k + 1 - 1;
					throw "fire";
				}

				if (abs(tmp_h1[i]) > 10e10) {
					k = k + 1 - 1;
					throw "h1 too big";
				}
				if (abs(tmp_h2[i]) > 10e10) {
					k = k + 1 - 1;
					throw "h2 too big";
				}

			}

			new_h1.push_back(tmp_h1);
			new_h2.push_back(tmp_h2);



			for (int i = 0; i < 2 * N - 1; i += 2) {
				if (i == 2 * N - 2 || i == 0) {
					tmp_u1[i] = u1[i];
					tmp_u2[i] = u2[i];
				}
				else {
					if (tmp_h1[i] <= 0.001) {
						tmp_u1[i] = 0;
					}
					else {
						tmp_u1[i] = (((P1[i + 1] - P1[i - 1]) / deltax -
							(u1[i + 1] * j1[i + 1] - u1[i - 1] * j1[i - 1]) / deltax -
							g / (2 * deltax) * (h1[i + 1] * h1[i + 1] - h1[i - 1] * h1[i - 1]) -
							g * (h1[i] - tau1[i] / deltax * (h1[i + 1] * u1[i + 1] - h1[i - 1] * u1[i - 1])) *
							(r / deltax * (h2[i + 1] - h2[i - 1]) - r * tau2[i] / (deltax * deltax) * (h2[i + 2] * u2[i + 2] - 2 * h2[i] * u2[i] + h2[i - 2] * u2[i - 2]) + (b_points[i + 1] - b_points[i - 1]) / deltax)) *
							deltat + h1[i] * u1[i]) / tmp_h1[i];

						if (tmp_u1[i] != tmp_u1[i]) {
							k = k + 1 - 1;
							throw "fire";
						}
						if (abs(tmp_u1[i]) > 10e10) {
							k = k + 1 - 1;
							throw "u1 too big";

						}
					}
					if (tmp_h2[i] <= 0.001) {
						tmp_u2[i] = 0;
					}
					else {
						tmp_u2[i] = (((P2[i + 1] - P2[i - 1]) / deltax -
							(u2[i + 1] * j2[i + 1] - u2[i - 1] * j2[i - 1]) / deltax -
							g / (2 * deltax) * (h2[i + 1] * h2[i + 1] - h2[i - 1] * h2[i - 1]) -
							g * (h2[i] - tau2[i] / deltax * (h2[i + 1] * u2[i + 1] - h2[i - 1] * u2[i - 1])) *
							(1 / deltax * (h1[i + 1] - h1[i - 1]) - tau1[i] / (deltax * deltax) * (h1[i + 2] * u1[i + 2] - 2 * h1[i] * u1[i] + h1[i - 2] * u1[i - 2]) + (b_points[i + 1] - b_points[i - 1]) / deltax)) *
							deltat + h2[i] * u2[i]) / tmp_h2[i];

						if (abs(tmp_u2[i]) > 10e10) {
							k = k + 1 - 1;
							throw "u2 too big";
						}

						if (tmp_u2[i] != tmp_u2[i]) {
							k = k + 1 - 1;
							throw "fire";
						}


					}
				}


			}




			new_u1.push_back(tmp_u1);
			new_u2.push_back(tmp_u2);

			h1 = tmp_h1;
			h2 = tmp_h2;

			std::vector<float> tmp1(2 * N - 1);
			std::vector<float> tmp2(2 * N - 1);
			for (int i = 0; i < 2 * N - 1; i++) {
				tmp1[i] = deltax / sqrt(h1[i] * g);
				tmp2[i] = deltax / sqrt(h2[i] * g);
			}

			deltat = beta * std::min((*std::min_element(tmp1.begin(), tmp1.end())), (*std::min_element(tmp2.begin(), tmp2.end())));

			for (int i = 1; i < 2 * N - 1; i += 2) {
				h1[i] = (h1[i - 1] + h1[i + 1]) / 2.0f;
				h2[i] = (h2[i - 1] + h2[i + 1]) / 2.0f;
				u1[i] = (u1[i - 1] + u1[i + 1]) / 2.0f;
				u2[i] = (u2[i - 1] + u2[i + 1]) / 2.0f;

				if (h1[i] < 0) {
					h1[i] = 0;
				}
				if (h2[i] < 0) {
					h2[i] = 0;
				}


			}

			k += 1;
		}


		res.push_back(h1);
		res.push_back(h2);
		res.push_back(u1);
		res.push_back(u2);
		return(res);
	}
}
