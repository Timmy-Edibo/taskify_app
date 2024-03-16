document.onload = () => {
  console.log("Hello dear");
}
$(document).ready(() => {
  const results = [1, 2];

  console.log("Hello dear");

  jQuery.each(results, (k, v) => {
    console.log("Hello chief");
    $('tbody').append(`
    <tr class="shadow-black shadow-md mb-10 rounded-2xl">
      <td class="p-3 py-5">
        <div class="flex">
          <div class="flex justify-center items-center px-4">
            <img src="images/placeholder.svg" alt="" width="30">
          </div>
          <div>
            <h4 class="text-lg font-semibold">World Widelife Redesign</h4>
            <p>Oct 13, 2021</p>
          </div>
        </div>
      </td>
      <td class="p-3 py-5">3d, 12m</td>
      <td class="p-3 py-5">
        <h6><span>90</span>/<span>148</span></h6>
        <p>Tasks</p>
      </td>
      <td class="p-3 py-5">
        <div class="flex flex-col justify-center">
          <div class="flex text-blue-200 items-center mb-2">
            <svg width="16" height="16" class="block">
              <use xlink:href="#edit"></use>
            </svg>
            <span class="block">Progress</span>
          </div>
          <progress value="25" max="100" class="project-task h-1 w-24">
            <div pseudo="-webkit-progress-inner-element">
              <div pseudo="-webkit-progress-bar">
                <div pseudo="-webkit-progress-value"></div>
              </div>
            </div>
          </progress>
        </div>
      </td>
      <td class="p-3 py-5">
        <div class="flex">
          <div class="rounded-50">
            <img src="images/placeholder.svg" alt="" width="40" class="rounded-50">
          </div>
          <div class="rounded-50 ml-[-6px]">
            <img src="images/placeholder.svg" alt="" width="40" class="rounded-50">
          </div>
          <div class="flex justify-center items-center rounded-50 bg-red-200 w-10 h-10 ml-[-6px]">
            <p>+3</p>
          </div>
        </div>
      </td>
      <td class="p-3 py-5">
        <button>
          <svg width="16" height="16" class="">
            <use xlink:href="#edit"></use>
          </svg>
        </button>
      </td>
    </tr>
    <tr class="h-10"></tr>
  `);
  })
});
