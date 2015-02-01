// Main Javascript
$(function($) {
  var slider = $('#slider').slideReveal({
  	position: 'left',
  	speed: 600,
  	trigger: $('#trigger')
  	});
  // Sticky Header
  /*$('.sticky').sticky({
  		topSpacing: 0
  });*/

  // Insert hr after titles
  $('.title-block').after('<hr>')

  // Set publication-div background image with data-src

  // Set publication-wrapper:last-of-type to <hr>
  $('.publication').after('<hr>')
  
  // Fade out FLASH on click
  $('form').click(function() {  
      setTimeout(function() { $('.flash').slideUp(500) }, 250);
      // setTimeout(function() { $('.flash').fadeOut(1500) }, 1000);
    });
});

