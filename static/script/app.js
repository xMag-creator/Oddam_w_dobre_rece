document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
      this.setInstitutions();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;
      const institutions = e.target.parentElement.parentElement.previousElementSibling.querySelectorAll("li");
      institutions.forEach((element) => element.style.display='none');  // hide all records current list
      this.show5records(page, institutions);  // show five records
      e.target.parentElement.parentElement.querySelectorAll("a").forEach(element => element.classList.remove("active"));
      e.target.classList.add("active");
    }

    /**
     * Set first page for all institutions list
     */
    setInstitutions() {
      this.$el.querySelectorAll("ul.help--slides-items").forEach(institution => {
        const institutions = institution.querySelectorAll("li");
        institutions.forEach((element) => element.style.display='none');
        this.show5records(1, institutions);
        this.createPaginationButtons(institutions);
        institutions[0].parentElement.nextElementSibling.firstElementChild.querySelector("a").classList.add("active");
      });
    }

    /**
     * Show current records
     * @param page
     * @param recordList
     */
    show5records(page, recordList) {
      let startPos = Number(page) * 5;
      let repeats = 6;
      if (startPos > recordList.length) {
        repeats = 6 - (startPos - recordList.length);
        startPos = recordList.length;
      }
      for (let i=1; i<repeats; i++) {
        recordList[startPos - i].style.display='flex';
      }
    }

    /**
     * Create pagination button for each 5 institutions
     * @param recordList
     */
    createPaginationButtons(recordList) {
      const listLength = recordList.length;
      let repeats = listLength / 5;
      const pagination = recordList[0].parentElement.nextElementSibling;
      for (let i=0; i<repeats; i++) {
        const record = document.createElement("li");
        const button = document.createElement("a");
        button.classList.add("btn");
        button.classList.add("btn--small");
        button.classList.add("btn--without-border");
        button.innerText = `${i+1}`;
        button.dataset.page = `${i+1}`;
        record.appendChild(button);
        pagination.appendChild(record);
      }

    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          if (this.validation(this.currentStep)) {
            this.currentStep++;
            this.updateForm();
          }
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.$form.submit(e));

      // Filter institutions by chosen categories
      this.$form.querySelector('#secondNextButton').addEventListener("click", e => {
        const catArr = this.getCategories(e);
        this.noneDisplayInstitutionsStep3(e);
        this.displayCorrectInstitutions(e, catArr);
      });

      // Generate summary
      this.$form.querySelector("#fourthNextButton").addEventListener("click", e => {
        const institutionName = this.checkChosenInstitution(e);
        const bagsQuantity = this.getQuantityOfBags(e);
        const address = this.getAddress(e);
        this.updateSummary(e, institutionName, bagsQuantity, address);
      });
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {

      this.$step.innerText = this.currentStep;

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

    }

    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */
    submit(e) {
      e.preventDefault();
      this.currentStep++;
      this.updateForm();
    }

    /**
     * Get categories from first step
     * @param e
     * @returns {*[]}
     */
    getCategories(e) {
      const categories = []
      const categoriesCheckboxes = this.$form.querySelector("#step1").querySelectorAll("div.form-group--checkbox");
      categoriesCheckboxes.forEach((element) => {
        if(element.querySelector("input").checked){
          categories.push(element.querySelector("span.description").innerHTML);
        }
      });

      return categories
    }

    /**
     * Deactivate all div's in step 3
     * @param e
     */

    noneDisplayInstitutionsStep3(e) {
      const checkBoxes = this.$form.querySelector("#step3").querySelectorAll("div.form-group--checkbox");
      checkBoxes.forEach((element) => element.style.display='none');
    }

    /**
     * Show correct institutions
     * @param e
     * @param catArr
     */
    displayCorrectInstitutions(e, catArr) {
      const checkBoxes = this.$form.querySelector("#step3").querySelectorAll("div.form-group--checkbox");
      checkBoxes.forEach(element => {
        let matched = 0
        element.querySelectorAll("#category").forEach(element => {
          catArr.forEach(cat => {
            if(cat === element.innerHTML) {
              matched++;
            }
          });
        });
        if(matched === catArr.length) {
          element.style.display='block'
        }
      });
    }

    /**
     * Check which institution was chosen and return institution name
     * @param e
     * @return string
     */
    checkChosenInstitution(e) {
      let instName = "";
      this.$form.querySelectorAll("#step3 div.form-group--checkbox").forEach(element => {
        if(element.querySelector("input").checked) {
          instName = element.querySelector("div.title").textContent;
          return instName;
        }
      });
      return instName;
    }

    /**
     * Get quantity of bags to take
     * @param e
     * @return {string}
     */
    getQuantityOfBags(e) {
      return this.$form.querySelector("#step2").querySelector("input").value;
    }

    /**
     * Get address information
     * @param e
     * @return {*[]}
     */
    getAddress(e) {
      const newArr = []
      const inputs = this.$form.querySelector("#step4").querySelectorAll("input");
      inputs.forEach(element => {
        newArr.push(element.value);
      });
      const text = this.$form.querySelector("#step4").querySelector("textarea").value;
      if(text === "") {
        newArr.push("Brak uwag")
      }
      else {
        newArr.push(text);
      }
      return newArr;
    }

    /**
     * Update summary info
     * @param e
     * @param institutionName
     * @param bagsQuantity
     * @param address
     */
    updateSummary(e, institutionName, bagsQuantity, address) {
      const firstPart = this.$form.querySelector("#step5").querySelector("div.form-section").querySelectorAll("li");
      firstPart[0].querySelector("span.summary--text").innerHTML = bagsQuantity + " worki ubrań w dobrym stanie dla dzieci";
      firstPart[1].querySelector("span.summary--text").innerHTML = "Dla " + institutionName;
      let iter = 0;
      this.$form.querySelector("#step5").querySelectorAll("div.form-section")[1].querySelectorAll("li").forEach(element => {
        element.innerText = address[iter];
        iter++;
      });
    }

    validation(step) {
      if (step === 1) {
        return this.validateStep1();
      }
      else if (step === 2) {
        return this.validateStep2();
      }
      else if (step === 3) {
        return this.validateStep3();
      }
      else if (step === 4) {
        return this.validateStep4();
      }
    }

    validateStep1() {
      const categoriesCheckboxes = this.$form.querySelector("#step1").querySelectorAll("div.form-group--checkbox");
      let countCheckedCheckbox = 0
      categoriesCheckboxes.forEach(element => {
        if (element.querySelector("input").checked){
          countCheckedCheckbox++;
        }
      });
      return countCheckedCheckbox !== 0;
    }

    validateStep2() {
      const bags = parseInt(this.$form.querySelector("#step2").querySelector("input").value);
      return bags !== 0 && !(isNaN(bags));
    }

    validateStep3() {
      let instName = ''
      this.$form.querySelectorAll("#step3 div.form-group--checkbox").forEach(element => {
        if(element.querySelector("input").checked) {
          instName = element.querySelector("div.title").textContent;
          return instName;
        }
      });
      return instName !== '';
    }

    validateStep4() {
      let result = true;
      this.$form.querySelector("#step4").querySelectorAll("input").forEach(element => {
        if (element.value === "")  {
          result = false;
        }
      });
      return result
    }

  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }
});
