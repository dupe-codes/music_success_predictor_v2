Tweaking evaluation metric:

- Originally basing accuracy on raw value closeness within some threshold
- After analyzing data, thought better to do percentage closeness
- Tweaked thresholds of allowed percentage difference
    - thought process: How accurate do we gotta be to say we've reasonably predicted popularity?

- Our data is missing a key feature.. lol duh

- We still had some songs with 0 hotttnesss lingering in our data. Getting rid of them dropped us to 10000 songs

- Added in genre indicator
    - Helps with regular linear reg, but lasso seems to think genre does not tell us much
- Lets try data transforms maybe?

- With alpha =0.5
    Duration and year both are not set to zero. Cool?

- Categorize artist hottness

- Baseline results (lin reg + artist indicator): '
Predictor achieved a training error of 37.5117635987

R^2 score calculated by sklearn: 0.0

Testing linear model...
Baseline predictor achieved accuracy of 39.1476274165%
R^2 score calculated by sklearn: -0.00161172852692

- Nearest Neighbors w/ genre, duration, and year:
Predictor achieved training error of 39.5445134576

R^2 score calculated by sklearn: 0.143946012299


Testing neighbors model...
Neighbors predictor with basic features achieved accuracy of 36.5553602812%
R^2 score calculated by sklearn: -0.0768131786528
Done

- Linear Reg w/ Duration and Year:
   Training lasso model...
   Lasso model assigned following weights:
   [ 0.00012084 -0.00090584]



   Predictor achieved a training error of 37.398833051

   R^2 score calculated by sklearn: 0.0155695127019

   Testing lasso model...
   Lasso predictor with basic features achieved accuracy of 39.8066783831%
   R^2 score calculated by sklearn: 0.0241491229278
   Done

- Nearest Neighbors w/ Duration and Year:
    Predictor achieved training error of 39.6198004894

    R^2 score calculated by sklearn: 0.142848447168


    Testing neighbors model...
    Neighbors predictor with basic features achieved accuracy of 36.9068541301%
    R^2 score calculated by sklearn: -0.0839418015553
    Done

- L1 w/ Duration and Year:


- L1 run with full metadata:
    [  4.17429950e-05   0.00000000e+00   0.00000000e+00  -0.00000000e+00
      -0.00000000e+00   0.00000000e+00  -0.00000000e+00  -0.00000000e+00
         0.00000000e+00   0.00000000e+00]



         Predictor achieved a training error of 37.6058723885

         R^2 score calculated by sklearn: 0.00453978140743

         Testing lasso model...
         Lasso predictor with basic features achieved accuracy of 39.762741652%
         R^2 score calculated by sklearn: 0.00440056576989
         Done

- Lin Reg run with full metadata:
   Preparing data with basic features...
   Training lasso model...
   Lasso model assigned following weights: 
   [  1.22919056e-04   2.73550606e-01   2.70748374e-01  -1.03903178e-03
     -5.40591379e-06   3.76514086e-02   1.16233904e-02  -1.07912491e-03
        3.68242613e-05  -5.35515744e-04]



        Predictor achieved a training error of 41.8595896857

        R^2 score calculated by sklearn: 0.228467555072

        Testing lasso model...
        Lasso predictor with basic features achieved accuracy of 42.5307557118%
        R^2 score calculated by sklearn: 0.242013706387
        Done

- Lin reg run with duration, year, + genres:
    Ratio of popular songs correctly predicted: 0.0
    Ratio of unpopular songs correctly predicted: 1.0

- Average mean hotttnesss performs just as well LOL our features dont tell us shit
    Predictor achieved a training error of 38.208168643

    R^2 score calculated by sklearn: None

    Testing lasso model...
    Lasso predictor with basic features achieved accuracy of 39.0597539543%
    R^2 score calculated by sklearn: 0

    Ratio of popular songs correctly predicted: 0.0
    Ratio of unpopular songs correctly predicted: 1.0
