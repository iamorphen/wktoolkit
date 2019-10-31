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

  // Leveling up in WaniKani is achieved, at the time of this writing, by advancing radicals and kanji through a
  // certain review threshold. As such, the capabilities of this script cater toward ordering *lessons* by subject
  // type, leaving the user to work through all *reviews* in any order.

  const ReorderModalCSS = `
    .wktk-reorder-modal {
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

    .wktk-reorder-modal-content {
      background-color: #fff;
      margin: auto;
      padding: 20px;
      border: 1px solid #eee;
      width: 80%;
    }

    .wktk-reorder-modal-close {
      float: right;
      cursor: pointer;
    }
  `;

  /**
   * Prepends a Reorder indicator to the WaniKani stats list in lessons. This indicator can be clicked to open the
   * reordering configuration. Also creates the initially-hidden reordering configuration modal.
   * @return The reorder element (HTMLLIElement) added to the stats list.
   */
  const AddReorderElements = () => {
    // The reordering configuration modal.
    document.head.insertAdjacentHTML('beforeend', `<style>${ReorderModalCSS}</style>`);

    let reorder_modal = document.createElement('div');
    reorder_modal.id = 'wktk-reorder-modal';
    reorder_modal.classList.add('wktk-reorder-modal');

    let reorder_modal_content = document.createElement('div');
    reorder_modal_content.classList.add('wktk-reorder-modal-content');
    reorder_modal_content.innerHTML = 'TODO';

    let reorder_modal_close = document.createElement('span');
    reorder_modal_close.classList.add('wktk-reorder-modal-close');
    reorder_modal_close.innerHTML = '[close]';
    reorder_modal_close.onclick = event => reorder_modal.style.display = 'none';

    reorder_modal_content.append(reorder_modal_close);
    reorder_modal.append(reorder_modal_content);
    document.body.prepend(reorder_modal);

    // The visible Reorder control.
    let reorder_li = document.createElement('li');
    reorder_li.id = 'wktk-reorder-li';
    reorder_li.style.cursor = 'pointer';
    reorder_li.innerHTML = '[Reorder]';
    reorder_li.onclick = event => reorder_modal.style.display = 'block';

    document.getElementById('stats').querySelector('ul').prepend(reorder_li);

    return reorder_li;
  };

  const reorder_element = AddReorderElements();
})();
