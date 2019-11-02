// ==UserScript==
// @name         WaniKani Lesson Timer
// @namespace    https://wanikani.com
// @version      1.0
// @description  Display a timer in lessons
// @author       orphen
// @match        https://www.wanikani.com/lesson/session
// @grant        none
// ==/UserScript==

(function() {
  'use strict';

  // TODO(orphen) Save lesson timing statistics in persistent storage.
  // TODO(orphen) Refactor timer to enable freezing timer value in the UI when the user finishes the lesson and quiz.
  //              Also support timer state querying to avoid showing timer value after the quiz if timer is "off."

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

  /**
   * @return The time since the lesson started formatted as "00 m 00 s".
   */
  const DeltaTime = () => {
    const dt_s = (Date.now() - StartTime) / 1e3;
    const seconds = Math.trunc(dt_s % 60).toString().padStart(2, 0);
    const minutes = Math.trunc(dt_s / 60).toString().padStart(2, 0);
    return `${minutes} m ${seconds} s`;
  };

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

  const TimerOff = () => { document.getElementById(`${IDPrefix}-li`).innerHTML = '[Timer Off]'; };
  const TimerHidden = () => { document.getElementById(`${IDPrefix}-li`).innerHTML = '[Timer Hidden]'; };
  const TimerUpdate = () => { document.getElementById(`${IDPrefix}-li`).innerHTML = `[${DeltaTime()}]`; };

  /**
   * An interface to a timer that allows the user to step through timer behaviors. Users must call nextBehavior() at
   * least once to trigger a behavior from the list of managed behaviors.
   */
  class TimerManager {
    instance = null; // This class is a non-extensible singleton.

    /**
     * @p behaviors An array of TimerBehavior objects.
     */
    constructor(behaviors) {
      if (TimerManager.instance) { return TimerManager.instance; }

      TimerManager.instance = this;
      this.behaviors = behaviors;
      this.behaviorIndex = null;
      this.behaviorIntervalHandle = null;


      // Load timer configuration from persistant storage.
      const config = JSON.parse(localStorage.getItem(IDPrefix));
      if (config) {
        this.behaviorIndex = config.behaviorIndex - 1;
      }
    }

    nextBehavior() {
      if (this.behaviorIndex == null) {
        this.behaviorIndex = 0;
      } else {
        if (this.behaviorIntervalHandle) { clearInterval(this.behaviorIntervalHandle); }
        this.behaviorIndex = (this.behaviorIndex + 1) % this.behaviors.length;
      }
      this.behaviors[this.behaviorIndex].behavior();
      if (this.behaviors[this.behaviorIndex].recurring) {
        this.behaviorIntervalHandle = setInterval(this.behaviors[this.behaviorIndex].behavior, 1e3);
      }

      // Save timer configuration to persistant storage.
      localStorage.setItem(IDPrefix, JSON.stringify({behaviorIndex: this.behaviorIndex}));
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

  /**
   * Filters @p mutation_records for changes that suggest that the user has completed the quiz for a lesson. Then,
   * adds the total lesson and quiz time to the post-quiz message.
   * @p mutation_records a list of mutation records as provided by, for example, MutationObserver.
   */
  const TotalTimeDisplayFilter = mutation_records => {
    for (const record of mutation_records) {
      if (!record.target.classList.contains('hidden')) {
        // The div is no longer hidden, suggesting that the user has finished the quiz.
        let heading = record.target.querySelector('h1');
        heading.insertAdjacentHTML('afterbegin', `Lesson finished in ${DeltaTime()}.<br><br>`);
      }
    }
  };

  const timer_manager = new TimerManager([new TimerBehavior(TimerOff, false), new TimerBehavior(TimerHidden, false),
                                          new TimerBehavior(TimerUpdate, true)]);
  AddTimerElement(timer_manager);
  timer_manager.nextBehavior();

  let observer = new MutationObserver(TotalTimeDisplayFilter);
  observer.observe(document.getElementById('screen-lesson-ready'), { attributes: true });
  observer.observe(document.getElementById('screen-lesson-done'), { attributes: true });
})();
