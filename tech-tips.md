## Git/GitHub

### Collaborating on a Repository

Collaborating with git can be simple. You do not need to worry about branching, code reviews, pull requests, etc. if you are just working with a small group on a personal project.

1. [Create a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository) on one group member's account.
2. Invite other group members as [collaborators](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-user-account/managing-access-to-your-personal-repositories/inviting-collaborators-to-a-personal-repository) to the repository.
3. [Clone the repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) to each group member's computer.
4. When you make changes to the code:
   * Commit frequently.
   * Try not to include too many changes in one git commit.
   * Pull/push your _working_ code frequently.
   * Always write a meaningful git commit message.
   Read [these tips for creating meaningful git commits](https://reflectoring.io/meaningful-commit-messages/).

### Resolving Merge Conflicts

Code conflicts will be minimized if you remember to:
* Commit frequently.
* Try not to include too many changes in one git commit.
* Pull/push your _working_ code frequently.

However, unavoidably, eventually there will be some lines in your code that conflict with a collaborator's. Don't panic, this is normal. Read this [Atlassian Guide to Git Merge Conflicts](https://www.atlassian.com/git/tutorials/using-branches/merge-conflicts) (or you can skip straight to the sections on [identifying and resolving conflicts](https://www.atlassian.com/git/tutorials/using-branches/merge-conflicts#:~:text=How%20to%20identify%20merge%20conflicts)).

### Excellent Guides to Git

* [Beanstalk Guides](http://guides.beanstalkapp.com)
* [Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials)
* [GitHub Guides Quickstart](https://docs.github.com/en/get-started/quickstart)
* [Git Cheatsheet](https://education.github.com/git-cheat-sheet-education.pdf) (it's dense)
* **And, for when you're in a bind: [Git happens! 6 Common Git mistakes and how to fix them](https://about.gitlab.com/blog/2018/08/08/git-happens/)**

## Mapping in JS

While there is a lot of depth to creating really fancy map visualizations, creating basic interactive maps in a web page is mostly copy-paste. Here are some snippets that will help:

### Put a Leaflet map on a page

In your head, add:
```html
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"
 integrity="sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A=="
 crossorigin=""/>

<style>
  #map1 {
    height: 250px;
  }
</style>
```

In your body, where you want the map to show up, add:
```html
<div id="map1"></div>
```

At the end of your body, add:
```html
<script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"
 integrity="sha512-XQoYMqMTK8LvdxXYG3nZ448hOEQiglfqkJs1NOQV44cWnUrBc8PkAOcXy20w0vlaXaVUearIOBhiXZ5V3ynxwA=="
 crossorigin=""></script>

<script>
  var initialCenter = [40, -75.2];  // <-- Latitude, Longitude
  var initialZoom = 11;
  var map1 = L.map('map1').setView(initialCenter, initialZoom);

  var baseLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  });
  baseLayer.addTo(map1);
</script>
```

## Use a different base layer

[Stamen](http://maps.stamen.com/) produced some nice map tiles that they make available for free. Paste the following code into the appropriate place above (where it says `var baseLayer =`):

```js
var baseLayer = new L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/toner/{z}/{x}/{y}{r}.{ext}', {
	attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
	subdomains: 'abcd',
	minZoom: 0,
	maxZoom: 20,
	ext: 'png'
});
baseLayer.addTo(map1);
```

[Esri](http://leaflet-extras.github.io/leaflet-providers/preview/#filter=Esri) also provides tiles that you can use:

```js
var baseLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
	attribution: 'Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012'
});
baseLayer.addTo(map1);
```

Check out a whole library of tile providers at the [leaflet-providers](https://leaflet-extras.github.io/leaflet-providers/preview/) package.

### Add a GeoJSON-formatted data layer

After adding the base layer to the map, add the following code:

```js
var mapdata = /* Your GeoJSON goes here */;
var dataLayer = L.geoJSON(mapdata)
dataLayer.addTo(map);
```

OR, if your GeoJSON is available on the web with URL:

```js
var dataLayer = L.geoJSON(mapdata)
dataLayer.addTo(map);

// Your GeoJSON URL goes below...
fetch('https://storage.googleapis.com/mjumbewu_musa_509/lab08_maps_and_charts_in_html/mapdata.json')
.then(response => response.json())
.then(mapdata => {
  dataLayer.addData(mapdata)
});
```

* Leaflet's documentation on [Using GeoJSON](https://leafletjs.com/examples/geojson/).
* More information about GeoJSON (from HERE): [An Introduction to GeoJSON](https://developer.here.com/blog/an-introduction-to-geojson)
