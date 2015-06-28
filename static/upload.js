$(function() {
    $('#post-image').submit(function(event) {
      event.preventDefault();
      $('#images').html("");
      $.ajax({
          type: 'POST',
          url: post_image_url,
          data: $(this).serialize(),
          success: function (result) {
              if (result) {
                  console.log(result.result);

                  var content = '<p>' + JSON.stringify(result) + '</p><br>'+
                  "<img src=http://ec2-52-5-124-92.compute-1.amazonaws.com:8000"+result.result.images.orig+"/>"+
                  "<img src=http://ec2-52-5-124-92.compute-1.amazonaws.com:8000"+result.result.images.base+"/>"+
                  "<img src=http://ec2-52-5-124-92.compute-1.amazonaws.com:8000"+result.result.images.point1+"/>"+
                  "<img src=http://ec2-52-5-124-92.compute-1.amazonaws.com:8000"+result.result.images.point2+"/>"
                  $('#images').html(content);
              }
          },
          error: function(result) {
            $('#images').html("Error!");
          }
      })
  });
})