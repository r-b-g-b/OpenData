Ideas:
Incorporate a model of what different target variables mean.
For example, a vote means explicit approval for the project.
A view means general interest, and a combination of positive and negative.
A comment means extreme interest, but could be extreme positive or extreme negative.
(Looking at the data, it's clear that num_comments are not very well predicted by the Features,
this could be because a comment indicates someone who shows strong interest, but if it isn't
matched with a vote, it could mean strong disapproval). 
Possibly implement a HMM, with hidden nodes that are estimated from the Features described here.
General interest
Agreement
Disagreement

n = number of samples in the set

Run 1:
Linear Regression (sklearn.linear_model.LinearRegression)
Log10(depvars+10) ~ Bag of words + City + Tags + Source

Score: 0.6204

Run 2:
same as Run 1 but added Nchar

Score: 0.6224

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
