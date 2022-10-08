## Project Requirements
### Capabilities
* Perform sentiment analysis on the general twitter stream using the twitter stream API.
* Perform sentiment analysis on a given keyword to find sentiment of tweets containing that keyword.
* Display sentiment analysis in aggregate (as a histogram, chart, etc.).
* Display statistics about the sentiment analysis (accuracy, degree of certainty, etc.)
* Display sentiment analysis for a manually-selected group of tweets or individual tweet. 
* Can filter out tweets containing certain language or content (can be simply implemented through a filter). 

### User Experience
* User can start and stop the stream by clicking a "Start Stream" or "Stop Stream" button.
* User can choose at what point in the stream to run the sentiment analysis, by clicking a "Run Analysis" button.
* User can view tweets that the sentiment analysis is being conducted on. 
* User can select a single tweet to view their individual sentiment analysis.
* User can select multiple tweets to view the sentiment analysis of the group. 

## What (Summary)
To build this program, we are using the Twitter API to pull in a stream of tweets which are placed in a queue to be processed.  The list of tweets is processed by the deep learning model that has been fine tuned on sentiment classification.  The tweet ID is then given an associated sentiment prediction that is output to the stream.  The overall sentiment is held in a histogram to show the user the normal sentiment over the stream.

## How

### To get started contributing:
1. Check out the VS Code setup.
https://github.com/joshuam1008/media-analyzer/blob/main/docs/VSCode_Setup.md

2. Follow instructions for running the program as a developer.
https://github.com/joshuam1008/media-analyzer/blob/main/INSTALL.md

Steps also listed at https://github.com/joshuam1008/media-analyzer/blob/main/CONTRIBUTING.md

### To navigate the program

#### Common Use Case: Get Overall Stream Sentiment
1. Click "Start Sentiment" so that when the stream is started, sentiment information will be collected. 
2. Click "Start Stream".
The main stream will now populate with randomly sampled tweets from across all of twitter. Each red tweet is interpreted as negative, each gray tweet is neutral, and each green tweet is positive. 
You can additionally view the overall results of the stream in a histogram by clicking "Sentiment" under "Summary of Result". 

#### Common Use Case: Get Sentiment with Filtered Word
Example word: "sky"
1. Type "sky" into the text field and hit add.
2. Click "Start Sentiment" so that when the stream is started, sentiment information will be collected.
3. Click "Start Stream".
You will now see tweets populate on the main stream and on the filtered stream on the right. Each red tweet is interpreted as negative, each gray tweet is neutral, and each green tweet is positive. 




## Why
With Twitter and other social media platforms being a powerful tool for users to express their opinions on topics, we believe that marketing teams can use social media as a way to evaluate the public opinon on a product or feature.  We believe that a limitation in place is that these marketing teams can only processes a limited number of tweets / posts and the evaluation can be tedious.  With this in mind, we designed a tool that processes twitter streams to:
 - Predict the sentiment on thousands of tweets quickly
 - Show the sentiment of individual tweets
 - Filter by keywords
 - Filter by a language

This tool can be built upon to run sentiment on other social media platforms in a similar way and allow for limiting sentiment to sepcific accounts / topics. 
Other social media analysis tools exist, but the fact that ours runs in real time sets it apart. 

## Short Video
