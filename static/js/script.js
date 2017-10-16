/**
 * Created by denisbolshakov on 27/09/2017.
 */

$(document).ready(function () {

   $('#myForm').submit(function(e){

       e.preventDefault();
       $('#gallerie').html('');

     var team1 = $("#team1_id option:selected").val();
     var team2 = $("#team2_id option:selected").val();

      /* $.ajax({
          url:'/get_rating',
           data: {team1:$("#team1_id option:selected").val(),
               team2:$("#team2_id option:selected").val()
           }

       }).done(function (data) {
           $('#rating_img').html(data);
      });
      */
       //var img2 = new Image()

       var img;
       var div;

       /*
        img.src = "/get_image"
       //<img src="/get_image" width="500">
        $('#image').append(img);
*/
       // rating image:
        img = new Image();
        div = $("<div>");
        div.addClass("image_block");
        img.src = "/get_rating?team1="+encodeURIComponent(team1)+"&team2="+encodeURIComponent(team2);
        div.append($("<h5>Image for get_rating</h5>"));
        div.append(img);
        $('#gallerie').append(div);

        // positional rating img:
        img = new Image();
        div = $("<div>");
        div.addClass("image_block");
        img.src = "/get_positional_rating?team1="+encodeURIComponent(team1)+"&team2="+encodeURIComponent(team2);
        div.append($("<h5>Image for get_positional_rating</h5>"));
        div.append(img);
        $('#gallerie').append(div);

       return false;
   });

   $('#team2_id').change((e)=> {
        team2 = $("#team2_id option:selected").val();
        $("#team1_id option").each( (i,o)=> {
            console.log(o)
            if($(o).val() == team2){
                $(o).attr('disabled','disabled').siblings().removeAttr('disabled');
            }
        });
       console.log(e);
   });
   $('#team1_id').change((e)=> {
        team1 = $("#team1_id option:selected").val();
        $("#team2_id option").each( (i,o)=> {
            console.log(o)
            if($(o).val() == team1){
                $(o).attr('disabled','disabled').siblings().removeAttr('disabled');
            }
        });
       console.log(e);
   });

});

