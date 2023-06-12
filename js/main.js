// function updateVisitCount() {
//   // Check if the visit count exists in the local storage
//   if (localStorage.getItem('visitCount')) {
//     // Increment the visit count by 1
//     var count = parseInt(localStorage.getItem('visitCount'));
//     count++;
//     localStorage.setItem('visitCount', count);
//   } else {
//     // Set the visit count to 1 if it doesn't exist
//     localStorage.setItem('visitCount', 1);
//   }
  
//   // Display the visit count on the page
//   var visitCount = localStorage.getItem('visitCount');
//   var visitCountEle = document.getElementById('visit-count');
//   visitCountEle.innerHTML = visitCount;
//   console.log(visitCountEle);
// }

// // Call the function to update the visit count on page load
// updateVisitCount();
(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();
    
    
    // Initiate the wowjs
    new WOW().init();


    // Facts counter
    $('[data-toggle="counter-up"]').counterUp({
        delay: 10,
        time: 2000
    });


    // Typed Initiate
    if ($('.typed-text-output').length == 1) {
        var typed_strings = $('.typed-text').text();
        var typed = new Typed('.typed-text-output', {
            strings: typed_strings.split(', '),
            typeSpeed: 100,
            backSpeed: 20,
            smartBackspace: false,
            loop: true
        });
    }


    // Smooth scrolling to section
    $(".btn-scroll").on('click', function (event) {
        if (this.hash !== "") {
            event.preventDefault();
            
            $('html, body').animate({
                scrollTop: $(this.hash).offset().top - 0
            }, 1500, 'easeInOutExpo');
        }
    });
    
    
    // Skills
    $('.skill').waypoint(function () {
        $('.progress .progress-bar').each(function () {
            $(this).css("width", $(this).attr("aria-valuenow") + '%');
        });
    }, {offset: '80%'});


    // Portfolio isotope and filter
    var portfolioIsotope = $('.portfolio-container').isotope({
        itemSelector: '.portfolio-item',
        layoutMode: 'fitRows'
    });
    $('#portfolio-flters li').on('click', function () {
        $("#portfolio-flters li").removeClass('active');
        $(this).addClass('active');

        portfolioIsotope.isotope({filter: $(this).data('filter')});
    });


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1500,
        dots: true,
        loop: true,
        items: 1
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });
})(jQuery);

// form validation
//     function validateForm(event) {
// event.preventDefault(); // Prevent the form from submitting automatically

// // Get form fields
// var name = document.getElementById("name").value;
// var email = document.getElementById("email").value;
// var subject = document.getElementById("subject").value;
// var message = document.getElementById("message").value;

// // Perform validation
// if (name.trim() === "") {
// showValidationMessage("Please enter your name.");
// return false;
// }

// if (email.trim() === "") {
// showValidationMessage("Please enter your email.");
// return false;
// }

// if (subject.trim() === "") {
// showValidationMessage("Please enter the subject.");
// return false;
// }

// if (message.trim() === "") {
// showValidationMessage("Please enter your message.");
// return false;
// }

// // All fields are valid, allow form submission
// event.target.submit(); // Manually submit the form
// }

// function showValidationMessage(message) {
// var validationPopup = document.getElementById("validation-popup");
// validationPopup.textContent = message;
// validationPopup.style.opacity = 1;
// setTimeout(function() {
// validationPopup.style.opacity = 0;
// }, 2000); // Hide the message after 2 seconds (adjust the duration as needed)
// }

// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
    'use strict'
  
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation')
  
    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
      .forEach(function (form) {
        form.addEventListener('submit', function (event) {
          if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
          }
  
          form.classList.add('was-validated')
        }, false)
      })
  })()

// sound on click
  function playClickSound() {
    var audio = document.getElementById("clickSound");
    audio.play();
    }
