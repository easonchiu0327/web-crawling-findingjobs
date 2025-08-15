using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Web;
using web_crawling_findingjobs.JobListData;

namespace web_crawling_findingjobs.JobListLogic.JobUtils
{
    public class JobUtilities
    {
        // Logic Tier passes the request for Data on to the DAO layer of the Data Teir

        // sellecting all
        public List<Job> SelectAllJob()
        {
            JobListDAO jobListDAO = new JobListDAO();
            return jobListDAO.JobSelectAll();
        }

        // for random sellect
        public List<Job> SelectRandomJob()
        {
            int rand = new Random().Next(98) + 1;///?????
            JobListDAO jobListDAO = new JobListDAO();
            return jobListDAO.JobRandomSelect(rand);
        }

        //select by category
        public List<Job> SelectByCategory(int categoryId)
        {
            JobListDAO jobListDAO = new JobListDAO();
            return jobListDAO.JobSelectByCategory(categoryId);
        }

        //select by citizenPR status
        public List<Job> SelectByCitizenPR(int citizenPRId)
        {
            JobListDAO jobListDAO = new JobListDAO();
            return jobListDAO.JobSelectByCitizenPR(citizenPRId);
        }

        //select by comapny
        public List<Job> SelectByCompany(int companyId)
        {
            JobListDAO jobListDAO = new JobListDAO();
            return jobListDAO.JobSelectByCompany(companyId);
        }

      
    }
}