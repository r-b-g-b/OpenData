n = number of samples in the set

Run 1:
Linear Regression (sklearn.linear_model.LinearRegression)
Log10(depvars+10) ~ Bag of words + City + Tags + Source

Score: 0.6204

Run 2:
same as Run 1 but added Nchar

# Features
## Bag of words
Take the top 100 highest frequency words from the descriptions and make a matrix indicating the count for each word in the description for each sample (n samples x 100 words matrix)

## City
Which city the sample came from

## Number of characters in the description

## Tags
An encoded and binarized matrix of tag occurance for each sample (n samples x 43 unique tags)

## Source
An encoded and binarized matrix of source occurance for each sample (n samples x 9 unique sources)
