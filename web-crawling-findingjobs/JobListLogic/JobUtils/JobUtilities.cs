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

        // sellecting all
        public List<Job> SellectALL()
        {
            JobListDAO jobListDAO = new JobListDAO();
            return jobListDAO.JobSellectAll();
        }

        // for random sellect
        public List<Job> SellectRandomJob()
        {
            int rand = new Random().Next(98) + 1;///?????
            JobListDAO jobListDAO = new JobListDAO();
            return jobListDAO.JobRandomSellect(rand);
        }
    }
}