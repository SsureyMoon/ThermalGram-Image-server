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
                 var publicDNS = "http://ec2-54-208-206-110.compute-1.amazonaws.com";
                 console.log(result.result);
                 var content = '<h3>' + "Result" + '</h3>' +
                 '<p>' + JSON.stringify(result) + '</p><br>'+
                 "<img src="+publicDNS+result.result.images.orig+">"+
                 "<img src="+publicDNS+result.result.images.base+">"+
                 "<img src="+publicDNS+result.result.images.point1+">"+
                 "<img src="+publicDNS+result.result.images.point2+">";
                  $('#images').html(content);
              }
          },
          error: function(result) {
            $('#images').html("Error!");
          }
      })
  });
})