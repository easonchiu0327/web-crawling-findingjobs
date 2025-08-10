using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using web_crawling_findingjobs.JobListData;

namespace web_crawling_findingjobs.JobListLogic.JobUtils
{
    public class JobUtilities
    {
        // Logic Tier passes the request for Data on to the DAO layer of the Data Teir
        public List<Job> SellectALL()
        {
            JobListDAO jobListDAO = new JobListDAO();
            return jobListDAO.JobSellectAll();
        }
    }
}