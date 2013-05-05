$(function(){
  $('#container').masonry({
    // options
    itemSelector : '.thumb',
    columnWidth : 240
  });
});

var $container = $('#thumbContainer');
$container.imagesLoaded(function(){
  $container.masonry({
    itemSelector : '.thumb',
    columnWidth : 240
  });
});


