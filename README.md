[![testing](https://github.com/joshuam1008/media-analyzer/actions/workflows/django.yml/badge.svg)](https://github.com/joshuam1008/media-analyzer/actions/workflows/django.yml) 
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7154682.svg)](https://doi.org/10.5281/zenodo.7154682)
[![License](https://img.shields.io/github/license/joshuam1008/media-analyzer)](https://github.com/joshuam1008/media-analyzer/blob/main/LICENSE)
[![Release](https://img.shields.io/github/v/release/joshuam1008/media-analyzer?include_prereleases)](https://github.com/joshuam1008/media-analyzer/releases/tag/v0.0.1)

# Media Analyzer
A Twitter stream sentiment analyzer written in Python.

# [Documentation](https://github.com/joshuam1008/media-analyzer/blob/main/docs/index.md)

# Pending Development Plan
| Iteration 1                | Iteration 2                       | Iteration 3               | Iteration 4              | Iteration 5            | Iteration 6   |
| -------------------------- | --------------------------------- | ------------------------- | ------------------------ | ---------------------- | ------------- |
| Display Twitter stream     | Filter Twitter stream by language | Single sentiment Analysis | Filter stream by keyword | Filter stream by topic | Bot detection |
| Overall sentiment on stream |                                   |                           |                          |                        |               |
|                            |                                   |                           |                          |                        |               |

deployment 
https://sheltered-citadel-93242.herokuapp.com/twitter/
currently using server side rendering, thus need to refresh page to get new stream

api 
post "/twitter/fetch_result"
1.fetch_result type post
expected json in backend

{"id":[id1,id2,id3],"category":['stream','sentiment','lang en']}

id represent result of twitter you requested on.
category is the type of result you requested.
stream: if you request stream, the data in stream cache will be fetched along with other results you requested in category

expected response for front end

{"stream":[id:{'sentiment':0,'lang':'en'}....],"inds": ["id1":{'sentiment':0,'lang':'en'}, "id2":{'sentiment':None,'lang':None}....]}

I seperate stream with requested tweet so the stream can be appended to frontend easier.
None means the backend will give it to you in the future.
so in the next round you can call again to get the result.

{"id":[id],"category":['stream','sentiment','lang en']}


