using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace web_crawling_findingjobs.JobListLogic.CompanyUtils
{
    public class Company
    {
        private int company_id;
        private string name;

        public Company()
        {
        }

        public Company(int company_id, string name)
        {
            this.company_id = company_id;
            this.name = name;
        }

        public int Company_id { get => company_id; set => company_id = value; }
        public string Name { get => name; set => name = value; }

    }
}