using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using web_crawling_findingjobs.JobListData;

namespace web_crawling_findingjobs.JobListLogic.CategoryUtils
{
    public class CategoryUtilities
    {
        public List<Category> SelectAll()
        {
            JobListDAO jobListDAO = new JobListDAO();
            return jobListDAO.CategorySelectAll();
        }
    }
}