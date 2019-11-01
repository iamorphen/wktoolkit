// ==UserScript==
// @name         WaniKani Lesson Timer
// @namespace    https://wanikani.com
// @version      0.1
// @description  Display a timer in lessons
// @author       orphen
// @match        https://www.wanikani.com/lesson/session
// @grant        none
// ==/UserScript==

(function() {
  'use strict';

  // TODO(orphen) Add persistent state for the configuration of the timer element.
  // TODO(orphen) Add total elapsed time to end-of-lesson page.

  const IDPrefix = 'wktk-lesson-timer';

  const TimerCSS = `
    <style>
    #${IDPrefix}-li {
      cursor: pointer;
    }
    </style>
  `;
  const TimerHTML = `<li id='${IDPrefix}-li'>[Timer]</li>`;

  const StartTime = Date.now();

  class TimerBehavior {
    /**
     * @p behavior A function to invoke as the timer behavior.
     * @p recurring If true, this behavior should be invoked on some interval.
     */
    constructor(behavior, recurring) {
      this.behavior = behavior;
      this.recurring = recurring;
    }
  };

  const TimerOff = new TimerBehavior(() => { document.getElementById(`${IDPrefix}-li`).innerHTML = '[Timer Off]'; },
                                     false);
  const TimerHidden = new TimerBehavior(
    () => { document.getElementById(`${IDPrefix}-li`).innerHTML = '[Timer Hidden]'; }, false);
  const TimerLive = new TimerBehavior(
    () => {
      let dt_s = (Date.now() - StartTime) / 1e3;
      let seconds = Math.trunc(dt_s % 60).toString().padStart(2, 0);
      let minutes = Math.trunc(dt_s / 60).toString().padStart(2, 0);
      document.getElementById(`${IDPrefix}-li`).innerHTML = `[${minutes} m ${seconds} s]`;
    }, true);

  class TimerManager {
    /**
     * @p behaviors An array of TimerBehavior objects.
     */
    constructor(behaviors) {
      this.behaviors = behaviors;
      this.behaviorIndex = null;
      this.behaviorIntervalHandle = null;
    }

    nextBehavior() {
      if (this.behaviorIndex == null) {
        this.behaviorIndex = 0;
        this.behaviors[this.behaviorIndex].behavior();
        if (this.behaviors[this.behaviorIndex].recurring) {
          this.behaviorIntervalHandle = setInterval(this.behaviors[this.behaviorIndex].behavior, 1e3);
        }
      } else {
        if (this.behaviorIntervalHandle) { clearInterval(this.behaviorIntervalHandle); }
        this.behaviorIndex = (this.behaviorIndex + 1) % this.behaviors.length;
        this.behaviors[this.behaviorIndex].behavior();
        if (this.behaviors[this.behaviorIndex].recurring) {
          this.behaviorIntervalHandle = setInterval(this.behaviors[this.behaviorIndex].behavior, 1e3);
        }
      }
    }
  };

  /**
   * Prepends a timer element to the WaniKani stats list in lessons. The element behavior can be toggled by clicking on
   * the element.
   * @p timer_manager An instance of TimerManager, used for cycling the timer behavior.
   */
  const AddTimerElement = timer_manager => {
    document.head.insertAdjacentHTML('beforeend', TimerCSS);
    document.getElementById('stats').querySelector('ul').insertAdjacentHTML('afterbegin', TimerHTML);
    document.getElementById(`${IDPrefix}-li`).onclick = event => { timer_manager.nextBehavior(); };
  };

  const timer_manager = new TimerManager([TimerOff, TimerHidden, TimerLive]);
  AddTimerElement(timer_manager);
  timer_manager.nextBehavior();
})();
