## Energy-Expenditure-Estimation-Algorithm 
Infants, athletes, the elderly and all other humans share
 the common requirement for energy in the form of calories
 to function day-to-day. Total Daily Energy Expenditure (TDEE)
 is the number of calories an individual burns per day and is
 commonly referred to as “maintenance calories”.  This is because
 if an individual ate the amount of calories equivalent to their TDEE,
 they would maintain their weight. For anyone with health, physique
 or sports performance related goals, knowing their TDEE is essential
 for optimizing nutrition in a way that will align with their goals.

The most common method of estimating TDEE is through various TDEE prediction
 equations. The problem with these equations is that they are often inaccurate
 by hundreds of calories. These inaccurate calculations cause people to over
 or underestimate their caloric need. Therefore, more accurate estimation
 techniques are needed. 

Machine learning is a powerful tool used for data analysis. It is a form
 of artificial intelligence that is predicated upon the idea that systems
 can learn from data, identify patterns in data and ultimately make decisions
 with minimal input from humans. Our goal is to develop machine learning
 programs that will yield an accurate and accessible method of TDEE estimation.
  
## Motivation 
The vast majority with the goal of improving their body composition or
 sports performance by tracking calories will initially use an online
 calculator. A common issue with this approach is that the equations
 used by these calculators can be inaccurate. If we use a common search
 engine, Google, and search for a “TDEE calculator” we can see the
 Mifflin-St Jeor equation (Mifflin et al, 1990) and the Katch-McArdle
 equation (McArdle et al, 1986) are often used. These prediction equations
 are just two of the many methods of TDEE estimation that have resulted
 from past research. 
 
The traditional equations can be very inaccurate.  For example, one study on
  weightlifters (Joseph et al, 2017) determined how well prediction equations
  measure energy expenditure. Ultimately the authors found that all prediction equations
  provided a significant underestimation of energy expenditure for the study participants.
  The equation with the most accurate estimation was on average off by 375 calories,
  while the least accurate equation was off by an average of 636 calories. To put
  this into scope, it would not be unrealistic for an individual in a deficit or surplus
  of 600 plus calories to change their body weight by 5 or more pounds in a month.
  This is a significant difference between these subjects actual TDEE and their estimated
  TDEE based on the results of the prediction equations.
  
Other methods of estimating TDEE exist that are more accurate, such as the doubly labeled water method
 (DLW). DLW is considered the gold standard for measuring energy expenditure but is inaccessible to most
 individuals. This is because DLW is mainly used for research purposes because it is expensive and places
 a clinical burden on the individual being analyzed (Buchowski 2014). Another option for TDEE estimation
 is to utilize regression models developed from prior research. Many models have been created with varying
 degrees of accuracy, however many of these models are buried in the literature and not easily accessible
 to the general population. Take for example a meta analysis from 2013 that noted “In practice, application
 of a best fitting model  is also limited by data availability. While fat free mass, fat mass, and waist and
 hip circumference are significant predictors, these variables may not be available to researchers or individuals.”
 (Sabounchi et al, 2013). Even if an individual were to find the research paper detailing a given model, they may
 not even have enough data about themselves to apply it practically.

The following quote from an article detailing energy requirements predicted from DLW summarizes why an individual 
should be aware of their TDEE  “An initial estimate of energy requirements remains integral to all weight change 
interventions, and the best possible prediction based on the available measurements should be employed” (Plucker et al, 2018).
 However, it is not always practical to implement “the best possible prediction based on the available measurements”. This
 leaves an opportunity for an easily accessible and accurate method of TDEE estimation to be developed.

## Built With 
-Python (https://www.python.org/) 
	-pandas (https://pandas.pydata.org/) 
	-NumPy (https://numpy.org/)
	-scikit-learn (https://scikit-learn.org/stable/)
		-Tool1.2.1 (link_to_tool) 
  
-Google Firebase (https://firebase.google.com/) 
	-Firebase cloud functions (https://firebase.google.com/docs/functions) 
 
## Project Results  
https://logsmarter.net/#/ 
