using System;
using System.Collections.Generic;
using System.Configuration;
using System.Data.SqlClient;
using System.Drawing;
using System.Linq;
using System.Web;
using System.Web.UI.WebControls;
using Microsoft.Ajax.Utilities;
using web_crawling_findingjobs.JobListLogic.CategoryUtils;
using web_crawling_findingjobs.JobListLogic.CitizenPR;
using web_crawling_findingjobs.JobListLogic.CompanyUtils;
using web_crawling_findingjobs.JobListLogic.JobUtils;

namespace web_crawling_findingjobs.JobListData
{
    public class JobListDAO
    {
        public List<Job> JobSelectAll()
        {
            List<Job> jobList = new List<Job>();
            // Directly get the connection string from Web.config
            string connectionString = ConfigurationManager.ConnectionStrings["DefaultConnection"].ConnectionString;

            SqlConnection conn = new SqlConnection(connectionString);
            SqlCommand cmd = new SqlCommand();
            cmd.Connection = conn;
            cmd.CommandText = "SELECT * FROM JobListings";
            using (conn)
            {
                conn.Open();
                SqlDataReader reader = cmd.ExecuteReader();

                while (reader.Read())
                {
                    jobList.Add(
                        new Job(
                            (int)reader["Id"],
                            (string)reader["Company"],
                            (string)reader["JobTitle"],
                            (string)reader["Location"],
                            (string)reader["Category"],
                            (string)reader["Skills"],
                            (string)reader["Years"],
                            (string)reader["CitizenPR"],
                            (string)reader["Link"]
                        ));
                }
                conn.Close();
            }
            return jobList;
        }

        public List<Job> JobRandomSelect(int rand)
        {
            List<Job> jobList = new List<Job>();
            // Directly get the connection string from Web.config
            string connectionString = ConfigurationManager.ConnectionStrings["DefaultConnection"].ConnectionString;

            SqlConnection conn = new SqlConnection(connectionString);
            SqlCommand cmd = new SqlCommand();
            cmd.Connection = conn;
            cmd.CommandText = @"
SELECT TOP 1
  JobListings.Id,
  Company.Name AS Company,
  JobListings.JobTitle,
  JobListings.Location,
  JobListings.Skills,
  JobListings.Years,
  JobListings.Link,
  Category.Category AS Category,
  CitizenPR.CitizenPR AS CitizenPR
FROM JobListings
LEFT JOIN Company   ON Company.Company_id     = JobListings.Company_id
LEFT JOIN Category  ON Category.Category_id   = JobListings.Category_id
LEFT JOIN CitizenPR ON CitizenPR.CitizenPR_id = JobListings.CitizenPR_id
ORDER BY CHECKSUM(NEWID(), @RandValue)";
            cmd.Parameters.AddWithValue("@RandValue", rand);
            using (conn)
            {
                conn.Open();
                SqlDataReader reader = cmd.ExecuteReader();

                while (reader.Read())
                {
                    jobList.Add(
                        new Job(
                            (int)reader["Id"],
                            (string)reader["Company"],
                            (string)reader["JobTitle"],
                            (string)reader["Location"],
                            (string)reader["Category"],
                            (string)reader["Skills"],
                            (string)reader["Years"],
                            (string)reader["CitizenPR"],
                            (string)reader["Link"]
                        ));
                }
                conn.Close();
            }
            return jobList;
        }


        public List<Category> CategorySelectAll()
        {
            List<Category> categories = new List<Category>();
            // Directly get the connection string from Web.config
            string connectionString = ConfigurationManager.ConnectionStrings["DefaultConnection"].ConnectionString;

            SqlConnection conn = new SqlConnection(connectionString);
            SqlCommand cmd = new SqlCommand();
            cmd.Connection = conn;
            cmd.CommandText = "SELECT * FROM Category";
            using (conn)
            {
                conn.Open();
                SqlDataReader reader = cmd.ExecuteReader();

                while (reader.Read())
                {
                    categories.Add(
                        new Category(
                            (int)reader["Category_id"],
                            (string)reader["Category"]
                        ));
                }
                conn.Close();
            }
            return categories;
        }

        //since I normalized your JobListings table:
        //Split Company, Category, and CitizenPR into separate tables.
        //Added foreign keys: Company_id, Category_id, CitizenPR_id inside JobListings.
        public List<Job> JobSelectByCategory(int categoryId)
        {
            List<Job> jobList = new List<Job>();

            // Directly get the connection string from Web.config
            string connectionString = ConfigurationManager.ConnectionStrings["DefaultConnection"].ConnectionString;

            SqlConnection conn = new SqlConnection(connectionString);
            SqlCommand cmd = new SqlCommand();
            cmd.Connection = conn;
            // SQL query based on categoryId
            if (categoryId == 0) // Return all movies if categoryId is 0 ("All Categories")
            {
                cmd.CommandText = @"
SELECT
  JobListings.Id,
  Company.Name AS Company,
  JobListings.JobTitle,
  JobListings.Location,
  JobListings.Skills,
  JobListings.Years,
  JobListings.Link,
  Category.Category AS Category,
  CitizenPR.CitizenPR AS CitizenPR
FROM JobListings
LEFT JOIN Company   ON Company.Company_id     = JobListings.Company_id
LEFT JOIN Category  ON Category.Category_id   = JobListings.Category_id
LEFT JOIN CitizenPR ON CitizenPR.CitizenPR_id = JobListings.CitizenPR_id";
            }
            else // Filter by specific category
            {
                cmd.CommandText = @"
SELECT
  JobListings.Id,
  Company.Name AS Company,
  JobListings.JobTitle,
  JobListings.Location,
  JobListings.Skills,
  JobListings.Years,
  JobListings.Link,
  Category.Category AS Category,
  CitizenPR.CitizenPR AS CitizenPR
FROM JobListings
LEFT JOIN Company   ON Company.Company_id     = JobListings.Company_id
LEFT JOIN Category  ON Category.Category_id   = JobListings.Category_id
LEFT JOIN CitizenPR ON CitizenPR.CitizenPR_id = JobListings.CitizenPR_id
WHERE JobListings.Category_id = @Category_id";
                cmd.Parameters.AddWithValue("@Category_id", categoryId);
            }

            using (conn)
            {
                conn.Open();
                SqlDataReader reader = cmd.ExecuteReader();

                while (reader.Read())
                {
                    jobList.Add(
                        new Job(
                            (int)reader["Id"],
                            (string)reader["Company"],
                            (string)reader["JobTitle"],
                            (string)reader["Location"],
                            (string)reader["Category"],
                            (string)reader["Skills"],
                            (string)reader["Years"],
                            (string)reader["CitizenPR"],
                            (string)reader["Link"]
                        ));
                }
                conn.Close();
            }
            return jobList;
        }

        public List<CitizenPR> CitizenPRSelectAll()
        {
            List<CitizenPR> citizenPRStatus = new List<CitizenPR>();
            // Directly get the connection string from Web.config
            string connectionString = ConfigurationManager.ConnectionStrings["DefaultConnection"].ConnectionString;

            SqlConnection conn = new SqlConnection(connectionString);
            SqlCommand cmd = new SqlCommand();
            cmd.Connection = conn;
            cmd.CommandText = "SELECT * FROM CitizenPR";
            using (conn)
            {
                conn.Open();
                SqlDataReader reader = cmd.ExecuteReader();

                while (reader.Read())
                {
                    citizenPRStatus.Add(
                        new CitizenPR(
                            (int)reader["CitizenPR_id"],
                            (string)reader["CitizenPR"]
                        ));
                }
                conn.Close();
            }
            return citizenPRStatus;
        }

        public List<Job> JobSelectByCitizenPR(int citizenPR_id)
        {
            List<Job> jobList = new List<Job>();

            // Directly get the connection string from Web.config
            string connectionString = ConfigurationManager.ConnectionStrings["DefaultConnection"].ConnectionString;

            SqlConnection conn = new SqlConnection(connectionString);
            SqlCommand cmd = new SqlCommand();
            cmd.Connection = conn;
            // SQL query based on CitizenPR_id
            if (citizenPR_id == 0) // Return all movies if CitizenPR_id is 0 ("All CitizenPR")
            {
                cmd.CommandText = "SELECT * FROM JobListings";
            }
            else // Filter by specific CitizenPR
            {
                cmd.CommandText = "SELECT * FROM JobListings WHERE CitizenPR_id = @CitizenPR_id";
                cmd.Parameters.AddWithValue("@CitizenPR_id", citizenPR_id);
            }

            using (conn)
            {
                conn.Open();
                SqlDataReader reader = cmd.ExecuteReader();

                while (reader.Read())
                {
                    jobList.Add(
                        new Job(
                            (int)reader["Id"],
                            (string)reader["Company"],
                            (string)reader["JobTitle"],
                            (string)reader["Location"],
                            (string)reader["Category"],
                            (string)reader["Skills"],
                            (string)reader["Years"],
                            (string)reader["CitizenPR"],
                            (string)reader["Link"]
                        ));
                }
                conn.Close();
            }
            return jobList;
        }

        public List<Company> CompanySelectAll()
        {
            List<Company> company = new List<Company>();
            // Directly get the connection string from Web.config
            string connectionString = ConfigurationManager.ConnectionStrings["DefaultConnection"].ConnectionString;

            SqlConnection conn = new SqlConnection(connectionString);
            SqlCommand cmd = new SqlCommand();
            cmd.Connection = conn;
            cmd.CommandText = "SELECT * FROM Company";
            using (conn)
            {
                conn.Open();
                SqlDataReader reader = cmd.ExecuteReader();

                while (reader.Read())
                {
                    company.Add(
                        new Company(
                            (int)reader["Company_id"],
                            (string)reader["Name"]
                        ));
                }
                conn.Close();
            }
            return company;
        }

        public List<Job> JobSelectByCompany(int company_id)
        {
            List<Job> jobList = new List<Job>();

            // Directly get the connection string from Web.config
            string connectionString = ConfigurationManager.ConnectionStrings["DefaultConnection"].ConnectionString;

            SqlConnection conn = new SqlConnection(connectionString);
            SqlCommand cmd = new SqlCommand();
            cmd.Connection = conn;
            // SQL query based on company_id
            if (company_id == 0) // Return all movies if company_id is 0 ("All companies")
            {
                cmd.CommandText = "SELECT * FROM Company";
            }
            else // Filter by specific company
            {
                cmd.CommandText = "SELECT * FROM JobListings WHERE Company_id = @Company_id";
                cmd.Parameters.AddWithValue("@Company_id", company_id);
            }

            using (conn)
            {
                conn.Open();
                SqlDataReader reader = cmd.ExecuteReader();

                while (reader.Read())
                {
                    jobList.Add(
                        new Job(
                            (int)reader["Id"],
                            (string)reader["Company"],
                            (string)reader["JobTitle"],
                            (string)reader["Location"],
                            (string)reader["Category"],
                            (string)reader["Skills"],
                            (string)reader["Years"],
                            (string)reader["CitizenPR"],
                            (string)reader["Link"]
                        ));
                }
                conn.Close();
            }
            return jobList;
        }
    }
}
