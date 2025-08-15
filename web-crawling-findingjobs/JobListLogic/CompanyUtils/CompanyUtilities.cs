using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using web_crawling_findingjobs.JobListData;

namespace web_crawling_findingjobs.JobListLogic.CompanyUtils
{
    public class CompanyUtilities
    {
        public List<Company> SelectAll()
        {
            JobListDAO jobListDAO = new JobListDAO();
            return jobListDAO.CompanySelectAll();
        }
    }
}