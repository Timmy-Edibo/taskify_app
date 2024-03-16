import './style.css';
import project from './project.html';
import $ from 'jquery';

initializePage(project);

const pages = new Map([
  ['project', project],
]);

$('a').on('click', function (e) {
  e.preventDefault();
  $('.nav-link').each((k, v) => {
    $(v).removeClass('active');
  });

  $(this).addClass('active');
  let pageRef = $(this).attr('href');

  console.log(pages.get(pageRef));

  $('script:not(".dependency")').remove()

  initializePage(pages.get(pageRef));
});

function initializePage(htmlString) {
  const parser = new DOMParser;
  const doc = parser.parseFromString(htmlString, 'text/html');

  // console.log('DOMParser', doc.querySelector('script').innerHTML);
  const content = doc.querySelector('.content');
  const script = doc.querySelector('script');

  $('#content').html(content);

  console.log('Here sha', htmlString);

  document.body.onload = () => {
    $('body').append(`<script>
        ${script.text}
      </script>
    `);
  };
}

/*function loadPage(pageRefInput) {
  $.ajax({
    url: pageRefInput,

    type: "GET",

    dataType: 'text',

    success: function (response) {
      console.log('the page was loaded', response);
      initializePage(response);
    },

    error: function (error) {
      console.log('the page was NOT loaded', error);
    },

    complete: function (xhr, status) {
      console.log("The request is complete!");
    }
  });
}*/
