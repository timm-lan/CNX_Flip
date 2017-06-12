$(document).ready(function() {
 // click to flip a card 
  $('.flashcard').on('click', function() {
    $('.flashcard').toggleClass('flipped');
  });

// press space key to flip a card 
  $(window).keypress(function(e){
      if (e.keyCode===32){
           $('.flashcard').toggleClass('flipped');
      }
      }
  )
  }
);