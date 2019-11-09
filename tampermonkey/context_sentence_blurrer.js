// ==UserScript==
// @name         WaniKani Vocabulary Context Sentence Blurrer
// @namespace    https://wanikani.com
// @version      1.0
// @description  Blurs vocabulary context sentences on WaniKani
// @author       orphen
// @match        https://www.wanikani.com/lesson/session
// @grant        none
// ==/UserScript==

(function() {
  'use strict';

  // This style is adapted from the element style WaniKani uses for spoilers in its forum.
  const BlurStyle = {
    'backgroundColor': 'transparent',
    'color': 'rgba(0, 0, 0, 0)',
    'textShadow': 'gray 0px 0px 10px',
    'userSelect': 'none',
  };

  /**
   * This blurs an HTML element's text content. It also adds mouseenter/leave handlers to toggle the blur.
   * @p element An instance of HTML*Element.
   */
  const AddBlurToElement = element => {
    const apply_blur = element => {
      for (const [k, v] of Object.entries(BlurStyle)) element.style[k] = v;
    };
    const remove_blur = element => {
      for (const k of Object.keys(BlurStyle)) element.style[k] = '';
    };

    element.onmouseenter = event => remove_blur(event.currentTarget);
    element.onmouseleave = event => apply_blur(event.currentTarget);
    apply_blur(element);
  };

  /**
   * Filter a list of mutation records for <p> elements that do not claim to have Japanese language content.
   * Call AddBlurToElement() for elements that pass filtering.
   * @p mutation_records A list of instances of MutationRecord as returned by, for example, MutationObserver.
   */
  const ElementBlurFilter = mutation_records => {
    for (const record of mutation_records) {
      if (record.type != 'childList') continue;
      for (const node of record.addedNodes) {
        node.querySelectorAll('p').forEach(element => {
          if (element.hasAttribute('lang') && element.getAttribute('lang') == 'ja') return;
          AddBlurToElement(element);
        });
      }
    }
  };

  const Main = () => {
    // The context sentences are dynamically loaded, so we have to react to modifications of them.
    const observer = new MutationObserver(ElementBlurFilter);
    observer.observe(document.getElementById('supplement-voc-context-sentence'), {
      childList: true,
      subtree: true,
    });
  };

  Main();
})();
