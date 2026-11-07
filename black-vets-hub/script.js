// Resource directory data. Add or edit entries here.
const CATEGORIES = {
  all: "All",
  benefits: "Benefits & Claims",
  health: "Health Care",
  mental: "Mental Health",
  housing: "Housing",
  jobs: "Jobs & Business",
  education: "Education",
  legal: "Legal & Discharge",
  family: "Family & Survivors",
};

const RESOURCES = [
  // Benefits & Claims
  { cat: "benefits", official: true, title: "VA Disability Compensation", desc: "Tax-free monthly payments for conditions caused or worsened by service. Start or check a claim.", url: "https://www.va.gov/disability/", phone: "800-827-1000" },
  { cat: "benefits", official: true, title: "Decision Reviews & Appeals", desc: "Disagree with a decision? Choose a supplemental claim, higher-level review, or Board appeal.", url: "https://www.va.gov/decision-reviews/" },
  { cat: "benefits", official: true, title: "PACT Act Benefits", desc: "Expanded benefits for burn pits, Agent Orange, and other toxic exposures. Many past denials can be refiled.", url: "https://www.va.gov/resources/the-pact-act-and-your-va-benefits/" },
  { cat: "benefits", official: true, title: "Find an Accredited Representative", desc: "Locate a free, VA-accredited claims agent, attorney, or Veterans Service Organization rep.", url: "https://www.va.gov/get-help-from-accredited-representative/" },
  { cat: "benefits", official: true, title: "VA Center for Minority Veterans", desc: "Connect with a Minority Veterans Program Coordinator at your local VA facility.", url: "https://www.va.gov/centerforminorityveterans/" },
  { cat: "benefits", official: false, title: "NABVETS Claims Assistance", desc: "National Association for Black Veterans service officers help file and track claims.", url: "https://www.nabvets.org/" },

  // Health
  { cat: "health", official: true, title: "Apply for VA Health Care", desc: "Enroll online, by phone, or in person. Coverage includes primary care, specialty care, and prescriptions.", url: "https://www.va.gov/health-care/apply-for-health-care-form-10-10ez/", phone: "877-222-8387" },
  { cat: "health", official: true, title: "Find a VA Location", desc: "Search VA medical centers, clinics, and Vet Centers near you.", url: "https://www.va.gov/find-locations/" },
  { cat: "health", official: true, title: "Toxic Exposure Screening", desc: "Free screening at VA health facilities for veterans enrolled in VA care.", url: "https://www.va.gov/resources/the-pact-act-and-your-va-benefits/" },
  { cat: "health", official: true, title: "Women Veterans Health", desc: "Dedicated care and a call center for women veterans.", url: "https://www.womenshealth.va.gov/", phone: "855-829-6636" },

  // Mental health
  { cat: "mental", official: true, title: "Veterans Crisis Line", desc: "Free, confidential, 24/7 support. Dial 988 then press 1, text 838255, or chat online.", url: "https://www.veteranscrisisline.net/", phone: "988, press 1" },
  { cat: "mental", official: true, title: "Vet Centers", desc: "Community-based counseling for combat veterans, survivors of military sexual trauma, and families.", url: "https://www.vetcenter.va.gov/", phone: "877-927-8387" },
  { cat: "mental", official: true, title: "PTSD Resources", desc: "Self-assessment tools, treatment options, and apps from the National Center for PTSD.", url: "https://www.ptsd.va.gov/" },
  { cat: "mental", official: true, title: "Make the Connection", desc: "Real stories from veterans about mental health and recovery.", url: "https://www.maketheconnection.net/" },

  // Housing
  { cat: "housing", official: true, title: "National Call Center for Homeless Veterans", desc: "Homeless or at risk? Call any time for immediate help.", url: "https://www.va.gov/homeless/", phone: "877-424-3838" },
  { cat: "housing", official: true, title: "VA Home Loans", desc: "Buy, build, or refinance with no down payment in many cases.", url: "https://www.va.gov/housing-assistance/home-loans/" },
  { cat: "housing", official: true, title: "HUD-VASH Vouchers", desc: "Rental assistance paired with VA case management for homeless veterans.", url: "https://www.va.gov/homeless/hud-vash.asp" },
  { cat: "housing", official: false, title: "Black Veterans for Social Justice", desc: "Transitional housing, supportive services, and job help in New York City.", url: "https://www.bvsj.org/" },

  // Jobs & business
  { cat: "jobs", official: true, title: "Veteran Readiness & Employment", desc: "Job training, education, and support for veterans with service-connected disabilities.", url: "https://www.va.gov/careers-employment/vocational-rehabilitation/" },
  { cat: "jobs", official: true, title: "Veteran-Owned Small Business Support", desc: "SBA programs, training, and Veterans Business Outreach Centers.", url: "https://www.sba.gov/business-guide/grow-your-business/veteran-owned-businesses" },
  { cat: "jobs", official: true, title: "Federal Jobs for Veterans", desc: "Veterans' preference and hiring authorities for federal careers.", url: "https://www.fedshirevets.gov/" },
  { cat: "jobs", official: true, title: "American Job Centers", desc: "Free career counseling with priority service for veterans.", url: "https://www.careeronestop.org/" },

  // Education
  { cat: "education", official: true, title: "GI Bill Benefits", desc: "Tuition, housing, and books for college, trade school, and apprenticeships.", url: "https://www.va.gov/education/" },
  { cat: "education", official: true, title: "GI Bill Comparison Tool", desc: "Compare schools and see how much your benefits cover.", url: "https://www.va.gov/education/gi-bill-comparison-tool/" },
  { cat: "education", official: false, title: "HBCU Veteran Programs", desc: "Many Historically Black Colleges and Universities have veteran resource offices and Yellow Ribbon participation. Ask the admissions office.", url: "https://www.va.gov/education/about-gi-bill-benefits/post-9-11/yellow-ribbon-program/" },

  // Legal
  { cat: "legal", official: true, title: "Discharge Upgrade Instructions", desc: "Step-by-step guide to apply for a discharge upgrade or correction.", url: "https://www.va.gov/discharge-upgrade-instructions/" },
  { cat: "legal", official: false, title: "National Veterans Legal Services Program", desc: "Free legal help with discharge upgrades, appeals, and benefits disputes.", url: "https://www.nvlsp.org/" },
  { cat: "legal", official: false, title: "The Veterans Consortium", desc: "Pro bono attorneys for appeals at the U.S. Court of Appeals for Veterans Claims.", url: "https://www.vetsprobono.org/" },
  { cat: "legal", official: true, title: "Request Military Records (DD-214)", desc: "Get your service records from the National Archives.", url: "https://www.archives.gov/veterans/military-service-records" },

  // Family
  { cat: "family", official: true, title: "Survivor & Dependent Benefits", desc: "Compensation, pension, and education benefits for spouses, children, and parents.", url: "https://www.va.gov/family-and-caregiver-benefits/" },
  { cat: "family", official: true, title: "Caregiver Support", desc: "Training, respite, and a support line for family caregivers.", url: "https://www.caregiver.va.gov/", phone: "855-260-3274" },
  { cat: "family", official: true, title: "Burial & Memorial Benefits", desc: "Burial in a national cemetery, headstones, and Presidential Memorial Certificates.", url: "https://www.va.gov/burials-memorials/" },
  { cat: "family", official: false, title: "Military OneSource", desc: "Free 24/7 support for service members, veterans in transition, and families.", url: "https://www.militaryonesource.mil/", phone: "800-342-9647" },
];

(function () {
  const grid = document.getElementById("resource-grid");
  const filtersEl = document.getElementById("filters");
  const search = document.getElementById("resource-search");
  const countEl = document.getElementById("result-count");
  let active = "all";

  // Build filter buttons
  Object.entries(CATEGORIES).forEach(([key, label]) => {
    const b = document.createElement("button");
    b.type = "button";
    b.className = "chip";
    b.dataset.cat = key;
    b.textContent = label;
    b.setAttribute("aria-pressed", key === active);
    b.addEventListener("click", () => setCategory(key));
    filtersEl.appendChild(b);
  });

  function setCategory(key) {
    active = key;
    filtersEl.querySelectorAll(".chip").forEach((c) =>
      c.setAttribute("aria-pressed", c.dataset.cat === key)
    );
    render();
  }

  function telHref(phone) {
    const digits = phone.replace(/\D/g, "");
    return digits.length === 10 ? "tel:1" + digits : "tel:" + digits.slice(0, 3);
  }

  function render() {
    const q = search.value.trim().toLowerCase();
    const list = RESOURCES.filter((r) => {
      const inCat = active === "all" || r.cat === active;
      const text = (r.title + " " + r.desc + " " + CATEGORIES[r.cat]).toLowerCase();
      return inCat && (!q || text.includes(q));
    });

    grid.innerHTML = "";
    list.forEach((r) => {
      const card = document.createElement("article");
      card.className = "resource";
      card.innerHTML = `
        <div class="resource-tags">
          <span class="tag">${CATEGORIES[r.cat]}</span>
          ${r.official ? '<span class="tag tag-official">Official VA / Gov</span>' : ""}
        </div>
        <h3></h3>
        <p></p>
        <div class="resource-links">
          <a class="link-primary" target="_blank" rel="noopener">Visit →</a>
          ${r.phone ? `<a class="link-phone" href="${telHref(r.phone)}">📞 ${r.phone}</a>` : ""}
        </div>`;
      card.querySelector("h3").textContent = r.title;
      card.querySelector("p").textContent = r.desc;
      card.querySelector(".link-primary").href = r.url;
      grid.appendChild(card);
    });

    countEl.textContent = list.length
      ? `Showing ${list.length} resource${list.length === 1 ? "" : "s"}`
      : "No matches. Try another word, or call 800-827-1000 for VA benefits help.";
  }

  search.addEventListener("input", render);

  // "Get started" cards and other jump links pre-filter the directory
  document.querySelectorAll("[data-jump]").forEach((el) =>
    el.addEventListener("click", () => {
      search.value = "";
      setCategory(el.dataset.jump);
    })
  );

  // Mobile nav
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.getElementById("site-nav");
  toggle.addEventListener("click", () => {
    const open = toggle.getAttribute("aria-expanded") === "true";
    toggle.setAttribute("aria-expanded", !open);
    nav.classList.toggle("open", !open);
  });
  nav.querySelectorAll("a").forEach((a) =>
    a.addEventListener("click", () => {
      toggle.setAttribute("aria-expanded", "false");
      nav.classList.remove("open");
    })
  );

  // Share
  const shareBtn = document.getElementById("share-btn");
  const shareMsg = document.getElementById("share-msg");
  shareBtn.addEventListener("click", async () => {
    const data = { title: document.title, text: "Resources for African American veterans and families", url: location.href };
    try {
      if (navigator.share) {
        await navigator.share(data);
      } else {
        await navigator.clipboard.writeText(location.href);
        shareMsg.textContent = "Link copied. Pass it on.";
      }
    } catch (e) {
      shareMsg.textContent = "Copy this link: " + location.href;
    }
  });

  document.getElementById("year").textContent = new Date().getFullYear();
  render();
})();
