// ==UserScript==
// @name         WaniKani Lesson Reorder
// @namespace    https://wanikani.com
// @version      0.1
// @description  Reorder WaniKani subjects in lessons
// @author       orphen
// @match        https://www.wanikani.com/lesson/session
// @grant        none
// ==/UserScript==

(function() {
  'use strict';

  const IDPrefix = 'wktk-reorder';

  // Leveling up in WaniKani is achieved, at the time of this writing, by advancing radicals and kanji through a
  // certain review threshold. As such, the capabilities of this script cater toward ordering *lessons* by subject
  // type, leaving the user to work through all *reviews* in any order.

  const ReorderModalCSS = `
    <style>
    #${IDPrefix}-li {
      cursor: pointer;
    }

    .${IDPrefix}-modal {
      display: none;
      position: fixed;
      z-index: 1;
      padding-top: 100px;
      left: 0;
      top: 0;
      width: 100%;
      height: 100%;
      overflow: auto;
      background-color: rgba(0, 0, 0, 0.5);
    }

    .${IDPrefix}-modal-content {
      background-color: #fff;
      margin: auto;
      padding: 20px;
      border: 1px solid #eee;
      width: 80%;
    }

    .${IDPrefix}-modal-close {
      float: right;
      cursor: pointer;
    }

    .wktk-row:after {
      content: "";
      display: table;
      clear: both;
    }

    .wktk-col-25 {
      float: left;
      width: 15%;
      margin-top: 5px;
    }

    .wktk-col-75 {
      float: left;
      width: 85%;
      margin-top: 5px;
    }

    .wktk-col-75 span {
      margin-right: 10px;
    }
    </style>
  `;

  const ReorderControlHTML = `<li id='${IDPrefix}-li'>[Reorder]</li>`;

  // TODO(orphen) Factor in IDPrefix to attributes.
  const ReorderModalHTML = `
    <div id='${IDPrefix}-modal' class='${IDPrefix}-modal'>
      <div class='${IDPrefix}-modal-content'>
        <h1>Reorder Configuration</h1>
        <form id='${IDPrefix}-configuration-form'>
          <div class='wktk-row'>
            <div class='wktk-col-25'>Enabled</div>
            <div class='wktk-col-75'>
              <input type='checkbox' name='wktk-enabled' value='enabled' checked>
            </div>
          </div>
          <br>
          <div class='wktk-row'>
            <div class='wktk-col-25'><b>Order</b></div>
            <div class='wktk-col-75'><b>Subject</b></div>
          </div>
          <div class='wktk-row'>
            <div class='wktk-col-25'>First</div>
            <div class='wktk-col-75'>
              <span><input type='radio' name='wktk-first' value='radical'> Radical</span>
              <span><input type='radio' name='wktk-first' value='kanji'> Kanji</span>
              <span><input type='radio' name='wktk-first' value='vocabulary'> Vocabulary</span>
            </div>
          </div>
          <div class='wktk-row'>
            <div class='wktk-col-25'>Then</div>
            <div class='wktk-col-75'>
              <span><input type='radio' name='wktk-second' value='radical'> Radical</span>
              <span><input type='radio' name='wktk-second' value='kanji'> Kanji</span>
              <span><input type='radio' name='wktk-second' value='vocabulary'> Vocabulary</span>
            </div>
          </div>
          <div class='wktk-row'>
            <div class='wktk-col-25'>Finally</div>
            <div class='wktk-col-75'>?</div>
          </div>
        </form>
        <span id='${IDPrefix}-modal-close' class='${IDPrefix}-modal-close'>[close]</span>
      </div>
    </div>
  `;

  /**
   * Prepends a Reorder indicator to the WaniKani stats list in lessons. This indicator can be clicked to open the
   * reordering configuration. Also creates the initially-hidden reordering configuration modal.
   */
  const AddReorderElements = () => {
    document.getElementById('stats').querySelector('ul').insertAdjacentHTML('afterbegin', ReorderControlHTML);
    document.head.insertAdjacentHTML('beforeend', ReorderModalCSS);
    document.body.insertAdjacentHTML('afterbegin', ReorderModalHTML);

    // Modal element event handlers.
    const ModalElement = document.getElementById(`${IDPrefix}-modal`);
    document.getElementById(`${IDPrefix}-modal-close`).onclick = event => ModalElement.style.display = 'none';

    // Visible Reorder control event handlers.
    document.getElementById(`${IDPrefix}-li`).onclick = event => ModalElement.style.display = 'block';
  };

  const Main = () => {
    AddReorderElements();
  };

   Main();
})();
