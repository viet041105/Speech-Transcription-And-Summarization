CREATE DATABASE STTS

USE STTS

CREATE TABLE job_requests (
    id INT PRIMARY KEY IDENTITY(1,1),
    job_uid NVARCHAR(100) NOT NULL,   
    original_filename NVARCHAR(255), 
    file_path NVARCHAR(500),         
    status NVARCHAR(50),              
    full_text NVARCHAR(MAX),          
    summary NVARCHAR(MAX),               
    created_at DATETIME DEFAULT GETDATE(), 
    completed_at DATETIME            
);