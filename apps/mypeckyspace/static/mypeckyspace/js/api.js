var url = "https://api.nytimes.com/svc/topstories/v2/home.json";
  url += '?' + $.param({
    'api-key': "cfd0871be48648f988de8c033e7cd57d"
  });
  $.ajax({
    url: url,
    method: 'GET',
  }).done(function(result) {
    console.log(result);
  }).fail(function(err) {
    throw err;
});
