using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using web_crawling_findingjobs.JobListData;
using web_crawling_findingjobs.JobListLogic.CategoryUtils;

namespace web_crawling_findingjobs.JobListLogic.CitizenPR
{
    public class CitizenPRUtilities
    {
        public List<CitizenPR> SelectAll()
        {
            JobListDAO jobListDAO = new JobListDAO();
            return jobListDAO.CitizenPRSelectAll();
        }
    }
}