# geotext_matching
Tools for matching geo objects.

# Matching admin

Contains django app with admin site, to mark dataset with matches and dismatches.

In admin you can see results and download csv.

```
./manage.py migrate
./manage.py runserver 8000
```

The thing uses sqlite.

## Main page

```/index``` is the main page. It shows you the map (google or leaflet) with
rendered objects: an OSM object and objects nearest by geo coordinates.

The viewport is zoomed to a group of rendered OSM object and one nearest object.
So if you don't see all of them, mb you need to zoomout.

When you see something matched (I'd have been expecting that there is only
one match for every OSM object), you hit the number on your keyboard and
the page sends POST request to save the matching result (with mark=1) and
other nearest objects will be marked as dismatched (mark=0).

So basically, one hit gives you more N rows in DB, where N is number of nearest
neighbours. 1 matching row and N-1 dismatching.

When you don't see matching hotels, you'd hit 0. This creates N rows in DB
and all of them are dismatched.

If you'd like to just skip the rendered result, you hit spacebar. This
result in rerendering a new result.

After every hit of a number there is a browser message. It's a UX kostyl to
prevent misclicked rerendering.

## Admin

```/admin```

There's an admin site to control the process. At first you need to create
an Iteration thing. It's an abstraction to group the results somehow, in
case you'd like to use one marked dataset and wouldn't like to use another.

The main page always works with the last iteration.

When you misclick some of the results, you can fix it on "Marked Objects"
page.

Mark could be 0, 1 or 2. 2 is a reserved value for result to be merged.
0 stands for mismatch, 1 - for match.

# Objects match classifier

## geomatched_dataset

A script to perform geo match of objects of given dataset
and OSM objects (a filtered planet or region).

Outputs 5 nearest neighbours of an OSM object in one row.

```
python3 geomatched_dataset.py
```

File names and columns are hardcoded in script.

## objects match classifier

objects_matching.py is a script that learns a classifier using given
train dataset, then gets dataset to be classified, outputs the accuracy score
and serializes classifier to ./classifier.pkl

To serialize use "-serialize" and pass the train dataset filepath:
```
python3 ./objects_matching.py -serialize ../Downloads/dataset\(1\).csv
```

To match using previously pickled classifier pass path to geomatched objects
dataset (generated with geomatched_dataset.py).

```
python3 ./objects_matching.py ../hotels_geomatched.csv
```
It makes given data flat, then classifies and outputs matched result.
An OSM object can only be matched to one booking hotel, on the other hand
one booking hotel can be matched to multiple OSM objects.

## tests
accuracy_test shows the dummy classifier accuracy and given classifier accuracy.
