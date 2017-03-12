/*------------------------------------------------------------------
 Deft - Multiporpose Coming Soon Template

* Version       :  1
* Build Date    : 31 May 2016
* Last Update   : 3 June 2016
* Author        : CodeRare
* Primary use   : Coming Soon

Copyright (C) 2016 Coderare
-------------------------------------------------------------------*/

/*------------------------------------------------------------------
[Table of contents]

1. Twitter Feeds
2. Page Loading
3. Masonry Grid
4. Project Gallery
5. MagnificPopup
6. PhotoSwipe
7. Instagram feeds
8. Slider
9. Backgound img Appending
10. CountDown Timer
11. Subscribe Form
12. Contact Form
13. ScrollToTop

-------------------------------------------------------------------*/

$( document ).ready(function() {
    "use strict";


    $("#rightContent").mCustomScrollbar({
        axis: "y",
        theme: "minimal-dark",
        scrollbarPosition: 'outside',
        scrollInertia: 120,
        setHeight: '100%',
        setTop: 0,
    });

    $('#nav-icon1,#nav-icon2,#nav-icon3,#nav-icon4').click(function () {
        $(this).toggleClass('open');
    });


    /* ------------------------------------- */
    /* Page Loading    ................... */
    /* ------------------------------------- */

    $(".animsition").animsition({
        inClass: 'fade-in',
        outClass: 'fade-out',
        inDuration: 300,
        outDuration: 800,
        linkElement: '.a-link',
        // e.g. linkElement: 'a:not([target="_blank"]):not([href^="#"])'
        loading: true,
        loadingParentElement: 'body', //animsition wrapper element
        loadingClass: 'animsition-loading',
        loadingInner: '', // e.g '<img src="loading.svg" />'
        timeout: false,
        timeoutCountdown: 5000,
        onLoadEvent: true,
        browser: ['animation-duration', '-webkit-animation-duration'],
        // "browser" option allows you to disable the "animsition" in case the css property in the array is not supported by your browser.
        // The default setting is to disable the "animsition" in a browser that does not support "animation-duration".
        overlay: false,
        overlayClass: 'animsition-overlay-slide',
        overlayParentElement: 'body',
        transition: function (url) {
            window.location.href = url;
        }
    });

    $('body').on('animsition.inEnd', function () {
        $("#leftSide").addClass('instate');
    })

    /* ---------------------------------------------*/
    /* animations for subscribe form & rightside ...*/
    /* --------------------------------------------- */

    $(function () {
        var map = document.getElementById('map');
        var mapToggle = document.getElementById('mapToggle');
        var btnSwitch = $(mapToggle).children('#switch');
        var home = document.getElementById('home');
        var midAnimate = $(home).find('.mid');
        var slowAnimate = $(home).find('.slow');

        function toggleMap(mapToggle, btnSwitch, map, home, midAnimate, slowAnimate) {
            $(btnSwitch).toggleClass('active');
            $(map).toggleClass('active');
            $(home).toggleClass('hidden');
            $(midAnimate).removeClass('mid');
            $(slowAnimate).removeClass('slow');
        }

        $(mapToggle).on('click', function (event) {
            event.preventDefault();
            if (event.target.hash === '#toggle') {
                toggleMap(mapToggle, btnSwitch, map, home, midAnimate, slowAnimate);
            }
        });

    });

    $(function () {

        var parent = document.getElementById('parent');
        var leftSide = $(parent).children('#leftSide');
        var subscribe = $(parent).children('#subscribe');
        var rightSide = $(parent).children('#rightSide');
        var rightContent = $(rightSide).children('#rightContent');
        var moreInfoBtn = $(parent).find('#info');
        var closeBtn = $('<a href="#closesub"><i class="close-btn ion-close-round"></i></a>');
        var subOverlay = $('<div class="sub_overlay"></div>');

        function showSubscribe(event, leftSide, subscribe, closeBtn) {
            event.preventDefault();
            $(subscribe).addClass('fadeup');
            $(subOverlay).toggleClass('visible');

            $(subOverlay).on('click', function () {
                $(this).removeClass('visible');
                $(subscribe).removeClass('fadeup');
            });

            $(closeBtn).on('click', function (event) {
                event.preventDefault();
                $(subscribe).removeClass('fadeup');
                $(subOverlay).removeClass('visible');

            });
        }

        function showContent(event, leftSide, rightSide, rightContent, moreInfoBtn) {
            event.preventDefault();
            if ($(leftSide).hasClass('full-width')) {
                $(leftSide).toggleClass('drag11');
            } else {
                $(leftSide).toggleClass('drag5');
            }
            $(rightSide).toggleClass('expand');
            $(rightContent).toggleClass('showcontent');

            $(moreInfoBtn).children('i').toggleClass('ion-navicon-round');
            $(moreInfoBtn).children('i').toggleClass('ion-close-round');
        }

        function addingContent(moreInfoBtn, subscribe, closeBtn, subOverlay) {
            var infoIcon = $('<i class="ion-navicon-round menu pr10"></i>');
            $(moreInfoBtn).prepend(infoIcon);
            $(subscribe).children('.border').prepend(closeBtn);
            $(subscribe).before(subOverlay);
        }

        addingContent(moreInfoBtn, subscribe, closeBtn, subOverlay)


        $(parent).on('click', function (event) {
            if (event.target.hash === '#info' || event.target.classList.contains('menu')) {
                showContent(event, leftSide, rightSide, rightContent, moreInfoBtn);
            } else if (event.target.hash === '#subscribe' || event.target.classList.contains('subs')) {
                showSubscribe(event, leftSide, subscribe, closeBtn);
            }
        });
    });


    /* ------------------------------------- */
    /* PhotoSwipe   ................... */
    /* ------------------------------------- */
    var initPhotoSwipeFromDOM = function (gallerySelector) {

        // parse slide data (url, title, size ...) from DOM elements
        // (children of gallerySelector)
        var parseThumbnailElements = function (el) {
            var thumbElements = el.childNodes,
                numNodes = thumbElements.length,
                items = [],
                figureEl,
                linkEl,
                size,
                item;

            for (var i = 0; i < numNodes; i++) {

                figureEl = thumbElements[i]; // <figure> element

                // include only element nodes
                if (figureEl.nodeType !== 1) {
                    continue;
                }

                linkEl = figureEl.children[0]; // <a> element

                size = linkEl.getAttribute('data-size').split('x');

                // create slide object
                item = {
                    src: linkEl.getAttribute('href'),
                    w: parseInt(size[0], 10),
                    h: parseInt(size[1], 10)
                };


                if (figureEl.children.length > 1) {
                    // <figcaption> content
                    item.title = figureEl.children[1].innerHTML;
                }

                if (linkEl.children.length > 0) {
                    // <img> thumbnail element, retrieving thumbnail url
                    item.msrc = linkEl.children[0].getAttribute('src');
                }

                item.el = figureEl; // save link to element for getThumbBoundsFn
                items.push(item);
            }

            return items;
        };

        // find nearest parent element
        var closest = function closest(el, fn) {
            return el && ( fn(el) ? el : closest(el.parentNode, fn) );
        };

        // triggers when user clicks on thumbnail
        var onThumbnailsClick = function (e) {
            e = e || window.event;
            e.preventDefault ? e.preventDefault() : e.returnValue = false;

            var eTarget = e.target || e.srcElement;

            // find root element of slide
            var clickedListItem = closest(eTarget, function (el) {
                return (el.tagName && el.tagName.toUpperCase() === 'FIGURE');
            });

            if (!clickedListItem) {
                return;
            }

            // find index of clicked item by looping through all child nodes
            // alternatively, you may define index via data- attribute
            var clickedGallery = clickedListItem.parentNode,
                childNodes = clickedListItem.parentNode.childNodes,
                numChildNodes = childNodes.length,
                nodeIndex = 0,
                index;

            for (var i = 0; i < numChildNodes; i++) {
                if (childNodes[i].nodeType !== 1) {
                    continue;
                }

                if (childNodes[i] === clickedListItem) {
                    index = nodeIndex;
                    break;
                }
                nodeIndex++;
            }


            if (index >= 0) {
                // open PhotoSwipe if valid index found
                openPhotoSwipe(index, clickedGallery);
            }
            return false;
        };

        // parse picture index and gallery index from URL (#&pid=1&gid=2)
        var photoswipeParseHash = function () {
            var hash = window.location.hash.substring(1),
                params = {};

            if (hash.length < 5) {
                return params;
            }

            var vars = hash.split('&');
            for (var i = 0; i < vars.length; i++) {
                if (!vars[i]) {
                    continue;
                }
                var pair = vars[i].split('=');
                if (pair.length < 2) {
                    continue;
                }
                params[pair[0]] = pair[1];
            }

            if (params.gid) {
                params.gid = parseInt(params.gid, 10);
            }

            return params;
        };

        var openPhotoSwipe = function (index, galleryElement, disableAnimation, fromURL) {
            var pswpElement = document.querySelectorAll('.pswp')[0],
                gallery,
                options,
                items;

            items = parseThumbnailElements(galleryElement);

            // define options (if needed)
            options = {

                // define gallery index (for URL)
                galleryUID: galleryElement.getAttribute('data-pswp-uid'),

                getThumbBoundsFn: function (index) {
                    // See Options -> getThumbBoundsFn section of documentation for more info
                    var thumbnail = items[index].el.getElementsByTagName('img')[0], // find thumbnail
                        pageYScroll = window.pageYOffset || document.documentElement.scrollTop,
                        rect = thumbnail.getBoundingClientRect();

                    return {x: rect.left, y: rect.top + pageYScroll, w: rect.width};
                }

            };

            // PhotoSwipe opened from URL
            if (fromURL) {
                if (options.galleryPIDs) {
                    // parse real index when custom PIDs are used
                    // http://photoswipe.com/documentation/faq.html#custom-pid-in-url
                    for (var j = 0; j < items.length; j++) {
                        if (items[j].pid == index) {
                            options.index = j;
                            break;
                        }
                    }
                } else {
                    // in URL indexes start from 1
                    options.index = parseInt(index, 10) - 1;
                }
            } else {
                options.index = parseInt(index, 10);
            }

            // exit if index not found
            if (isNaN(options.index)) {
                return;
            }

            if (disableAnimation) {
                options.showAnimationDuration = 0;
            }

            // Pass data to PhotoSwipe and initialize it
            gallery = new PhotoSwipe(pswpElement, PhotoSwipeUI_Default, items, options);
            gallery.init();
        };

        // loop through all gallery elements and bind events
        var galleryElements = document.querySelectorAll(gallerySelector);

        for (var i = 0, l = galleryElements.length; i < l; i++) {
            galleryElements[i].setAttribute('data-pswp-uid', i + 1);
            galleryElements[i].onclick = onThumbnailsClick;
        }

        // Parse URL and open gallery if it contains #&pid=3&gid=1
        var hashData = photoswipeParseHash();
        if (hashData.pid && hashData.gid) {
            openPhotoSwipe(hashData.pid, galleryElements[hashData.gid - 1], true, true);
        }
    };

// execute above function
    initPhotoSwipeFromDOM('.my-gallery');


    /* ------------------------------------- */
    /* Backgound img Appending................... */
    /* ------------------------------------- */

    $(function () {
        $('.background-img-holder').each(function () {
            var $imgSrc = $(this).children("img").attr("src");
            $(this).children("img").hide();
            $(this).css('background', 'url("' + $imgSrc + '")');
            $(this).css('background-size', 'cover');
            $(this).css('background-position', 'center');
            $(this).css('height', '100%');
        });
    });
});


/* ------------------------------------- */
/* CountDown Timer   ................... */
/* ------------------------------------- */

  // $('#timer')
  // .countdown($('#timer').attr("data-date")).on('update.countdown', function(event) {
  //    var $this = $(this).html(event.strftime(''
  //      + '<div class="clock-box"><span class="number"> %-D</span><span class="text"> Day%!d </span> </div>'
  //      + '<div class="clock-box"><span class="number"> %H</span><span class="text"> hours </span></div>'
  //      + '<div class="clock-box"><span class="number"> %M</span><span class="text"> minutes </span></div>'
        //  + '<div class="clock-box"><span class="simple"> %S</span>s  </div>'

  //      ));
  // });
  //
  // $('#timerTwo')
  // .countdown($('#timerTwo').attr("data-date")).on('update.countdown', function(event) {
  //    var $this = $(this).html(event.strftime(''
  //      + '<div class="clock-box"><span class="simple">%-D</span>d  </div>'
  //      + '<div class="clock-box"><span class="simple"> %H</span>h  </div>'
  //      + '<div class="clock-box"><span class="simple"> %M</span>m  </div>'
  //      ));
  // });


/* ------------------------------------- */
/* Subscribe Form   ................... */
/* ------------------------------------- */

// $(function() {
//
//
//   ajaxMailChimpForm($("#subscribe-form"), $("#subscribe-result"));
//   // Turn the given MailChimp form into an ajax version of it.
//   // If resultElement is given, the subscribe result is set as html to
//   // that element.
//   function ajaxMailChimpForm($form, $resultElement){
//
//       // Hijack the submission. We'll submit the form manually.
//       $form.submit(function(e) {
//           e.preventDefault();
//           if (!isValidEmail($form)) {
//               var error =  "A valid email address must be provided. Please check it and try again.";
//               $resultElement.removeClass('success');
//               setTimeout(function() {
//                 $resultElement.addClass('error');
//                 $resultElement.html(error);
//               }, 150);
//
//               setTimeout(function() {
//                 $resultElement.removeClass('error');
//               }, 2500);
//
//
//           } else {
//             $resultElement.removeClass('success');
//             $resultElement.removeClass('error');
//
//             setTimeout(function() {
//               if ( $('#subscribe').hasClass('vertical') ) {
//                 $('body').prepend('<div class="loading"></div>');
//               } else {
//                 $('#subscribe').append('<div class="loading"></div>');
//               }
//               submitSubscribeForm($form, $resultElement);
//             }, 150);
//
//
//           }
//       });
//   }
//   // Validate the email address in the form
//   function isValidEmail($form) {
//       // If email is empty, show error message.
//       // contains just one @
//       var email = $form.find("input[type='email']").val();
//       if (!email || !email.length) {
//           return false;
//       } else if (email.indexOf("@") == -1) {
//           return false;
//       }
//       return true;
//   }
//   // Submit the form with an ajax/jsonp request.
//   // Based on http://stackoverflow.com/a/15120409/215821
//   function submitSubscribeForm($form, $resultElement) {
//       $.ajax({
//           type: "GET",
//           url: $form.attr("action"),
//           data: $form.serialize(),
//           cache: false,
//           dataType: "jsonp",
//           jsonp: "c", // trigger MailChimp to return a JSONP response
//           contentType: "application/json; charset=utf-8",
//           error: function(error){
//             $resultElement.removeClass('success');
//
//             setTimeout(function() {
//               $resultElement.addClass('error');
//             }, 800);
//
//             setTimeout(function() {
//               $resultElement.removeClass('error');
//             }, 2500);
//
//               // According to jquery docs, this is never called for cross-domain JSONP requests
//           },
//           success: function(data){
//               if (data.result != "success") {
//                   var message = data.msg || "Sorry. Unable to subscribe. Please try again later.";
//                   if (data.msg && data.msg.indexOf("already subscribed") >= 0) {
//
//                       message = "You're already subscribed. Thank you.";
//                   }
//                   $resultElement.removeClass('error');
//                   $('#subscribe').children('.loading').remove();
//                   $('body').children('.loading').remove();
//
//
//                   setTimeout(function() {
//                     $resultElement.addClass('success');
//                     $resultElement.html(message);
//                   }, 150);
//
//                   setTimeout(function() {
//                     $resultElement.removeClass('success');
//                   }, 2500);
//
//
//               } else {
//                 $resultElement.removeClass('error');
//                 $('#subscribe').children('.loading').remove();
//                 $('body').children('.loading').remove();
//
//
//                 setTimeout(function() {
//                   $resultElement.addClass('success');
//                   $resultElement.html("Thank you! You must confirm the subscription in your inbox.");
//                 }, 150);
//
//                 setTimeout(function() {
//                   $resultElement.removeClass('success');
//                 }, 2500);
//
//               }
//           }
//       });
//   }
// });
//
// /* ------------------------------------- */
// /* Contact Form    ................... */
// /* ------------------------------------- */
//
//   $(function() {
//   	// Get the form.
//   	var form = $('#contact_form');
//
//   	// Get the messages div.
//   	var formMessages = $('#form-messages');
//     var formMessageSuccess = $('#form-messages .success');
//     var formMessageError = $('#form-messages .error');
//
//   	// Set up an event listener for the contact form.
//   	$(form).submit(function(e) {
//   		// Stop the browser from submitting the form.
//   		e.preventDefault();
//
//   		// Serialize the form data.
//   		var formData = $(form).serialize();
//
//   		// Submit the form using AJAX.
//   		$.ajax({
//   			type: 'POST',
//   			url: $(form).attr('action'),
//   			data: formData
//   		})
//   		.done(function(response) {
//   			// Make sure that the formMessages span or div has the 'success' class.
//         $('.success').fadeIn();
//         setTimeout(function(){
//           $('.success').fadeToggle(200,0);
//         },2500);
//         $('.error').fadeOut();
//   			// Set the message text.
//   			$(formMessageSuccess).text(response);
//
//   			// Clear the form.
//   			$('.input-name').val('');
//   			$('.input-email').val('');
//   			$('.input-message').val('');
//   		})
//   		.fail(function(data) {
//   			// Make sure that the formMessages span or div has the 'error' class.
//         $('.error').fadeIn();
//         setTimeout(function(){
//           $('.error').fadeToggle(200,0);
//         },2500);
//         $('.success').fadeOut();
//
//   			// Set the message text.
//   			if (data.responseText !== '') {
//   				$(formMessageError).text(data.responseText);
//   			} else {
//   				$(formMessageError).text('Oops! An error occured.');
//   			}
//   		});
//   	});
//   });
//
//
// });
