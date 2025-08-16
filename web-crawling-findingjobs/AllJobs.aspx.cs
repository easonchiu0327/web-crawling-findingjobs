using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using Antlr.Runtime;
using web_crawling_findingjobs.JobListLogic.JobUtils;

namespace web_crawling_findingjobs
{
    public partial class About : Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack) // Only run on first page load
            {
                ddlFilterCategory.SelectedValue = "0";
                ddlFilterCompany.SelectedValue = "0";
                ddlFilterCitizenPR.SelectedValue = "0";
                BindJobsFromFilters();
            }
        }

        protected void timerRandomJob_Tick(object sender, EventArgs e)
        {
            //called when timer ticks
            odjJobsRandom.Select();
            // re-bind the gridview data source
            grdRandomJob.DataBind();
        }

        // all three dropdowns call the same binder
        protected void ddlFilterCategory_SelectedIndexChanged(object s, EventArgs e) => BindJobsFromFilters();
        protected void ddlFilterCompany_SelectedIndexChanged(object s, EventArgs e) => BindJobsFromFilters();
        protected void ddlFilterCitizenPR_SelectedIndexChanged(object s, EventArgs e) => BindJobsFromFilters();

        //combined filters together
        private void BindJobsFromFilters()
        {
            //int.TryParse(string, out var c) safely tries to turn that string into an int.
            //If successful → returns true and stores the result in c.
            //If failed → returns false, and c is ignored.
            //? c : 0 means:
            //If parsing worked → use the parsed number.
            //If parsing failed → fall back to 0.
            int categoryId = int.TryParse(ddlFilterCategory.SelectedValue, out var c) ? c : 0;
            int companyId = int.TryParse(ddlFilterCompany.SelectedValue, out var m) ? m : 0;
            int citizenPRId = int.TryParse(ddlFilterCitizenPR.SelectedValue, out var p) ? p : 0;

            JobUtilities util = new JobUtilities();
            List<Job> jobs = util.SelectByFilters(categoryId, companyId, citizenPRId); 

            grdJobs.DataSource = jobs;
            grdJobs.DataBind();
        }
    }
}