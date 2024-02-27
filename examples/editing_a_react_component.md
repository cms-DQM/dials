# Editing a React component

This example depicts the train of thoughts to complete the TODO's item: "Create card with bad files count".

# Fetching data from the api

Following the [`Creating a Django ViewSet protected by CERN Auth`](examples/django_viewset_with_cern_auth.md) example we should have an api endpoint `/api/v1/bad-file-index`. From the Swagger view we can see that the following HTTP GET request,

```bash
curl -X 'GET' \
  'http://localhost:8000/api/v1/bad-file-index/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <<ACCESS TOKEN>>'
```

will generate the following response,

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "file_path": "/mnt/dqmio/store_data_Run2022E_ZeroBias_DQMIO_19Jan2023-v2_2550000_2AA7A92C-151F-4340-9546-E877B6F9895D.root",
      "data_era": "2022E",
      "st_size": 33554431,
      "st_ctime": "2024-02-09T21:19:59.954917Z",
      "st_itime": "2024-02-17T23:57:32.106789Z",
      "err": "OSError: Failed to open file <<fpath>>"
    }
  ]
}
```

and since we are interested in get the `count` we don't need to paginate the output. In `Node.js` it is easy to do HTTP request with the `Axios` liberary (it is like `requests` in python), jump to the file [`api.index.js`](frontend/src/services/api/index.js) and add the following code:

```javascript
const listBadFileIndex = async ({ page, era, minSize, pathContains }) => {
  const endpoint = `${API_URL}/bad-file-index/`
  const params = sanitizedURLSearchParams({
    page,
    era,
    min_size: !isNaN(minSize) ? parseInt(minSize) * (1024 ** 2) : undefined, // Transforming from MB (user input) to B
    path_contains: pathContains
  }, { repeatMode: false })
  const response = await axiosApiInstance.get(endpoint, {
    params
  })
  return response.data
}
```

Note that the requests are using a custom `axios` instance `axiosApiInstance` (in the same file you can check how it is defined), but in general it is intercepting the request event and appending the api access token so you don't need to wonder how to authenticate with the api via the frontend if you just use that object!

Now, from other files you can't import the new function `listBadFileIndex` because you need to `export` it like `export myFunc ...`, but for consistency instead of exporting multiple object this module is exporting an object with multiple functions all at once. Then, to export our new function from this module we need to append the following code to the `API` object:

```javascript
const API = {
  ...
  badFileIndex: {
    list: listBadFileIndex
  },
  ...
}
```

# Fetching data inside the component

We are going to display a card with the bad files count next to the files count in statistics page, navigate to the file [`dataIngestion.stats.js`](frontend/src/views/dataIngestion/stats.js) to see the React component `IngestionStatistics` (in a simplified way, React components are objects that generate HTML content dynamically through self-contained JavaScript code).

Using the `useState` hook we can create a variable that forces React to render the component again upon any modification, since we are going to fetch the number of bad files indexed when the user open the statistics page we can append the following code:

```javascript
const IngestionStatistics = () => {
  ...
  const [totalBadFiles, setTotalBadFiles] = useState(0)
  ...
}
```

Note that this variable stats as 0, but how can we change it dynamically? Our event is the component mount, i.e. when the user open the statistics page the components mounts the first time. We can catch that event using the `useEffect` hook, hopefully there is one already configured and just need to append the following code:

```javascript
useEffect(() => {
  ...
  const fetchTotalBadIndexedFiles = () => {
    API.badFileIndex.list({})
      .then(response => {
        setTotalBadFiles(response.count)
      })
      .catch(err => {
        console.error(err)
        toast.error('Failure to communicate with the API!')
      })
  }

  ...
  fetchTotalBadIndexedFiles()
  ...
}, [])

```

How is the useEffect hook reacting to the first time the components mount? The second argument `useEffect(setup, dependencies)` is called `dependencies` and is set to an empty array `[]`, that is how React interprets that the only condition for triggering this hook is in the first mount. Note that, if we wanted to make the component re-render everytime a variable change we could put an `useState` variable as the dependency of the `useEffect` hook.

See that when our hook executes, it we execute the defined function `fetchTotalBadIndexedFiles` and when the request is complete (we catch that whith `then`) we use the `setTotalBadFiles` hook from our `useState` to update the variable `totalBadFiles` value.

# Displaying the data

So we have already fetched the data and dynamically update an variable inside the component using `useState` and `useEffect`, what is missing? Actually displaying that variable! Remember when I said that React geneates HTML dynamically? That is true, the output of an React component is HTML code (you can see to output of the `return` statement). But different from raw HTML code, React can extend this notation and turn components into "HTML Tags".

In the beggining of the `return` statement we can append the following code,

```javascript
<Col sm={3}>
  <Card className='text-center'>
    <Card.Header>Bad Files</Card.Header>
    <Card.Body><h1>{totalBadFiles}</h1></Card.Body>
  </Card>
</Col>
```

and also change all other `Cols` column size configuration withing the same `Row` to

```javascript
<Col sm={3}>
```

Since we are using `react-bootstrap`, the components `Col`, `Card`, `Card.Header` and `Card.Body` are simply high-level abstraction of plain `Boostrap` classes with html tags. Inside our card body we are putting our variable `totalBadFiles` enclosed in the `<h1>` tag (note that React differs text from variables using the curly braces).

Voilà, check you browser see the modification: When statistics page mounts react will trigger the `useEffect` hook that will fetch data from the api and update the `totalBadFiles` via the `useState` hook, than when the components returns the dynamically generated HTML it will embed the value of this variables.
