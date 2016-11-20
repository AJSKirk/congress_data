# 2016 Congressional Vote by District

This script scrapes the election result provided by [Townhall.com](http://townhall.com/election/2016/results) to return a csv of the counts by party by district.

Note that some districts are uncontested. In these cases, votes are not counted and this script returns a count of 0. No 'true' zeros exist in the data.

Inspiration here goes to tonmcg's work on scraping the [presidential count](https://github.com/tonmcg/County_Level_Election_Results_12-16)
