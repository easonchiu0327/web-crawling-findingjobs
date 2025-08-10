using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace web_crawling_findingjobs
{
    public partial class About : Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {

        }

        protected void timerRandomJob_Tick(object sender, EventArgs e)
        {
            //called when timer ticks
            odsJobs.Select();
            // re-bind the ListView’s data source
            grdRandomJob.DataBind();
        }
    }
}