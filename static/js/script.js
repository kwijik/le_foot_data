/**
 * Created by denisbolshakov on 27/09/2017.
 */

$(document).ready(function () {

   $('#myForm').submit(function(e){

       e.preventDefault();
       $('#gallerie').html('');
       $('#tables').html('');

       $('#tables').append($("<h3>Last games of the teams</h3>"));
       var div_last_games = $("<div>").addClass('all_floats');
        $('#tables').append(div_last_games);

       $('#tables').append($("<h3>Duel table</h3>"));
       var div_duel_games = $("<div>").addClass('all_floats');
       $('#tables').append(div_duel_games);

       $('#tables').append($("<h3>General rating</h3>"));
       var div_general_rating = $("<div>").addClass('all_floats');
       $('#tables').append(div_general_rating);

       $('#tables').append($("<h3>Positional rating</h3>"));
       var div_positional_rating = $("<div>").addClass('all_floats');
       $('#tables').append(div_positional_rating);

     var team1 = $("#team1_id option:selected").val();
     var team2 = $("#team2_id option:selected").val();

      $.ajax({
          url:'/last_games_team1',
           data: {team1:team1,
               team2:team2
           }

       }).done(function (data) {
           div_last_games.append(data);
      });

       $.ajax({
          url:'/last_games_team2',
           data: {team1:team1,
               team2:team2
           }

       }).done(function (data) {
            div_last_games.append(data);
       });


     $.ajax({
          url:'/duel_table',
           data: {team1:team1,
               team2:team2
           }

       }).done(function (data) {
           div_duel_games.append(data);
      });

     $.ajax({
          url:'/rating_table',
           data: {team1:team1,
               team2:team2
           }

       }).done(function (data) {
           div_general_rating.append(data);
      });

     $.ajax({
          url:'/positional_rating_table',
           data: {team1:team1,
               team2:team2
           }

       }).done(function (data) {
           div_positional_rating.append(data);
      });

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
        div.append(img);
        div_general_rating.append(div);

        // positional rating img:
        img = new Image();
        div = $("<div>");
        div.addClass("image_block");
        img.src = "/get_positional_rating?team1="+encodeURIComponent(team1)+"&team2="+encodeURIComponent(team2);
        div.append(img);
        div_positional_rating.append(div);

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

