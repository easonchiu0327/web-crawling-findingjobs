using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace web_crawling_findingjobs.JobListLogic.CategoryUtils
{
    public class Category
    {
        private int category_id;
        private string categories;

        public Category()
        {
        }

        public Category(int category_id, string categories)
        {
            this.category_id = category_id;
            this.categories = categories;
        }

        public int Category_id { get=>category_id; set=>category_id = value; }
        public string Categories { get=>categories; set=>categories = value; }
    }
}