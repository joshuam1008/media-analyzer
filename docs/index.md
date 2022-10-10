## Project Documentation
Follow this link to view project documentation 👉    [click here](media_analyzer/index.html)

## Project Requirements
### Capabilities
* Perform sentiment analysis on the general twitter stream using the twitter stream API.
* Perform sentiment analysis on a given keyword to find sentiment of tweets containing that keyword.
* Display sentiment analysis in aggregate (as a histogram, chart, etc.).
* Can filter tweets containing certain language or content (can be simply implemented through a filter). 
* Support access by multiple users.
* Adding new module shouldn't require refactoring code or changing existing structure. 

### User Experience
* User can start and stop the stream by clicking a "Start Stream" or "Stop Stream" button.
* User can choose at what point in the stream to run the sentiment analysis, by clicking a "Run Analysis" button.
* User can view tweets that the sentiment analysis is being conducted on. 
* User can select a single tweet to view their individual sentiment analysis.
* User can select multiple tweets to view the sentiment analysis of the group. 

## What (Summary)
![social media analyzer design](https://user-images.githubusercontent.com/10794555/194788676-0fdc2058-1609-4e39-9733-e95d1c6c82ef.jpeg)

The Media Analyzer is a program we built using Django to process a stream of data. The goal of this program is to allow adding new natural language processing modules easily, without refactoring code and changing existing data pipelines. We did so by using an event-driven structure and used a background scheduler to handle events so that the website will always be responsive. Tweets from the stream will first be cached, then it will take each tweet out of the cache, getting results based on activated analyzers synchronously (getting sentiment, detecting language), and put it back into the cache. This process will be scheduled to run again once finished. Meanwhile cleaning the cache will be scheduled to run every 2 sec to clear the cache. When receiving an API call, requested data will be fetched from the cache or database. If the requested data doesn't exist None will be returned as a promise, and the analyzer will be scheduled to generate the result asynchronously. When the frontend receives data was None, it will request that data again. In this deployment we fine tuned a deep learning on sentiment classification. On the UI, the white tweet indicating no sentiment, gray is netural, green positive and red negative. The overall sentiment is held in a histogram to show the user the normal sentiment over the stream.

## How...

### ...to get started with contributing:
1. Check out the VS Code setup.
[https://github.com/joshuam1008/media-analyzer/blob/main/docs/VSCode_Setup.md](https://github.com/joshuam1008/media-analyzer/blob/main/docs/VSCode_Setup.md)

2. Follow instructions for running the program as a developer.
[https://github.com/joshuam1008/media-analyzer/blob/main/INSTALL.md](https://github.com/joshuam1008/media-analyzer/blob/main/INSTALL.md
)

Steps also listed at [https://github.com/joshuam1008/media-analyzer/blob/main/CONTRIBUTING.md](https://github.com/joshuam1008/media-analyzer/blob/main/CONTRIBUTING.md)

### ...to navigate the program:

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
You will now see tweets populate on the main stream and on the filtered stream on the right. Red tweets are negative, gray tweets are neutral, and green tweets are positive.




## Why
With Twitter and other social media platforms being a powerful tool for users to express their opinions on topics, we believe that marketing teams can use social media as a way to evaluate the public opinion on a product or feature.  We believe that a limitation in place is that these marketing teams can only processes a limited number of tweets / posts and the evaluation can be tedious.  With this in mind, we designed a tool that processes twitter streams to:
 - Predict the sentiment on thousands of tweets quickly
 - Show the sentiment of individual tweets
 - Filter by keywords
 - Filter by a language

This tool can be built upon to run sentiment on other social media platforms in a similar way and allow for limiting sentiment to specific accounts / topics.  It is also highly extensible and possible additional features include filtering by hashtags, mentions of a specific username, verified accounts, and more.
Other social media analysis tools exist, but the fact that ours runs in real time sets it apart. 

## Short Video
[Click here to watch video](https://youtu.be/gJXU_zx9r98)


👆
