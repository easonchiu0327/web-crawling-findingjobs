using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using web_crawling_findingjobs.JobListLogic.JobUtils;

namespace web_crawling_findingjobs
{
    public partial class About : Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack) // Only run on first page load
            {
                JobUtilities jobUtilities = new JobUtilities();
                List<Job> jobList = jobUtilities.SelectByCategory(0); // 0 means "All Categories"

                grdJobs.DataSource = jobList;
                grdJobs.DataBind();
            }
        }

        protected void timerRandomJob_Tick(object sender, EventArgs e)
        {
            //called when timer ticks
            odjJobsRandom.Select();
            // re-bind the gridview data source
            grdRandomJob.DataBind();
        }

        protected void ddlFilterCategory_SelectedIndexChanged(object sender, EventArgs e)
        {
            int categoryId = int.Parse(ddlFilterCategory.SelectedValue);

            JobUtilities jobUtilities = new JobUtilities();
            List<Job> jobList = jobUtilities.SelectByCategory(categoryId);

            grdJobs.DataSource = jobList;
            grdJobs.DataBind();
        }
    }
}