var url = "https://api.nytimes.com/svc/search/v2/articlesearch.json";
  url += '?' + $.param({
    'api-key': "cfd0871be48648f988de8c033e7cd57d",
    'q': "amazon"
  });
  $.ajax({
    url: url,
    method: 'GET',
  }).done(function(result) {
    console.log(result);
    for (var i = 1; i <= result.response.docs.length; i++) {
      // document.getElementById('news').innerHTML = i;
      $('#url').append('<a href=' + result.response.docs[i].web_url + '>' + result.response.docs[i].headline.print_headline + '</a>' + '<br>');
    }
  }).fail(function(err) {
    throw err;
});
