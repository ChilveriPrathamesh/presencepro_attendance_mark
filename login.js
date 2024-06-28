const mysql = require('mysql2');
const express = require('express');
const bodyParser = require('body-parser');
const bcrypt = require('bcrypt');
const path = require('path');
const multer = require('multer');
const { spawn } = require('child_process');
const cookieParser = require('cookie-parser');
const fs = require('fs');
const { PythonShell } = require('python-shell');
const ExcelJS = require('exceljs');
const { connect } = require('http2');


const app = express();
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json()); // Parse JSON bodies
app.use(express.static(path.join(__dirname, 'public')));
app.use("/assets", express.static("assets"));
const upload = multer({ dest: 'uploads/' });

const connection = mysql.createConnection({
    host: "aws-attendance.cz608aw60ypw.eu-north-1.rds.amazonaws.com",
    user: "admin",
    password: "Pratham2807",
    database: "presencepro"
});

// Connect to the database
connection.connect(function (error) {
    if (error) throw error;
    else console.log("Connected to database successfully!");
});

app.get("/", function (req, res) {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.post('/signup', async (req, res) => {
    try {
        let { name, email, pwd } = req.body;

        if (!name || !email || !pwd) {
            return res.status(400).send('Name, email, and password are required');
        }

        let hashedPassword = await bcrypt.hash(pwd, 10);

        const query = 'INSERT INTO loginuser (email, user_name, user_pwd) VALUES (?, ?, ?)';
        connection.query(query, [email, name, hashedPassword], (err, results) => {
            if (err) {
                console.error('Error inserting user: ', err);
                res.status(500).send('Internal Server Error');
                return;
            }
            res.redirect('/welcome');
        });

    } catch (e) {
        console.log(e);
        res.status(500).send('Internal Server Error');
    }
});

app.post('/login', (req, res) => {
    const { email, pwd } = req.body;

    if (!email || !pwd) {
        return res.status(400).send('Email and password are required');
    }

    const query = 'SELECT * FROM loginuser WHERE email = ?';
    connection.query(query, [email], async (err, results) => {
        if (err) {
            console.error('Error querying user: ', err);
            res.status(500).send('Internal Server Error');
            return;
        }
        if (results.length > 0) {
            const user = results[0];
            const match = await bcrypt.compare(pwd, user.user_pwd);
            if (match) {
                res.redirect('/welcome');
            } else {
                res.status(401).send('Invalid email or password');
            }
        } else {
            res.status(401).send('Invalid email or password');
        }
    });
});


app.post('/upload', upload.single('image'), (req, res) => {
    const { className, fullName } = req.body;
    const { filename, path: filePath } = req.file;
    const buffer = fs.readFileSync(filePath);

    // Ensure the base images directory exists
    const baseImagesDir = path.join(__dirname, 'images');
    if (!fs.existsSync(baseImagesDir)) {
        fs.mkdirSync(baseImagesDir, { recursive: true });
    }

    // Create directory for class if not exists
    const classDir = path.join(baseImagesDir, className);
    if (!fs.existsSync(classDir)) {
        fs.mkdirSync(classDir, { recursive: true });
    }

    // Move uploaded file to class directory
    const newPath = path.join(classDir, filename);
    fs.renameSync(filePath, newPath);

    // Check if the class name exists in the database
    connection.query('SELECT * FROM classes WHERE className = ?', [className], (err, results) => {
        if (err) {
            console.error('Database query error:', err);
            return res.status(500).json({ status: 'error', message: 'Internal Server Error' });
        }

        if (results.length > 0) {
            // Class already exists
            // Insert the image into the database
            connection.query('INSERT INTO images (filename, filepath, className, fullName, imageDb) VALUES (?, ?, ?, ?, ?)', [filename, newPath, className, fullName, buffer], (err, result) => {
                if (err) {
                    console.error('Error inserting image into database:', err);
                    return res.status(500).json({ status: 'error', message: 'Internal Server Error' });
                }
                console.log('Image uploaded and database updated');

                // Send JSON response to client with success message
                res.json({ status: 'success', message: 'Image uploaded successfully' });
            });
        } else {
            // Class does not exist, create a new entry
            connection.query('INSERT INTO classes (className) VALUES (?)', [className], (err, result) => {
                if (err) {
                    console.error('Error inserting class into database: ', err);
                    return res.status(500).json({ status: 'error', message: 'Internal Server Error' });
                }
                connection.query('INSERT INTO images (filename, filepath, className, fullName, imageDb) VALUES (?, ?, ?, ?, ?)', [filename, newPath, className, fullName, buffer], (err, result) => {
                    if (err) {
                        console.error('Error inserting image into database:', err);
                        return res.status(500).json({ status: 'error', message: 'Internal Server Error' });
                    }
                    console.log('Image uploaded, new class created, and database updated');

                    // Send JSON response to client with success message
                    res.json({ status: 'success', message: 'Image uploaded successfully' });
                });
            });
        }
    });
});

app.post('/display_known', (req, res) => {
    const { className } = req.body;

    connection.query('SELECT * FROM images WHERE className = ? ORDER BY fullName ASC', [className], (err, results) => {
        if (err) {
            console.error('Database query error:', err);
            return res.status(500).send('Internal Server Error');
        }

        let imageHtml = '';
        results.forEach((image) => {
            // Generate HTML for each image item with a delete button
            imageHtml += `
                <div class="image-item">
                    <h3>${image.fullName}</h3>
                    <img src="data:image/jpeg;base64,${Buffer.from(image.imageDb).toString('base64')}" alt="${image.filename}">
                    <br>
                    <button class="delete-btn" data-image-id="${image.id}" data-type="known">Delete</button>
                </div>
            `;
        });

        // Send HTML response with images and delete buttons
        res.send(`
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Images for Class: ${className}</title>
                <link rel="stylesheet" href="assets/display.css">
                <style>
                    .image-container {
                        display: flex;
                        flex-wrap: wrap;
                        gap: 20px;
                        justify-content: center;
                        padding: 20px;
                    }
                    .image-item {
                        background: white;
                        padding: 10px;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                        text-align: center;
                        width: calc(20% - 40px); /* Adjust width to display 5 images per row */
                        box-sizing: border-box;
                    }
                    .image-item img {
                        max-width: 100%;
                        height: auto;
                        border-radius: 5px;
                    }
                    .delete-btn {
                        background-color: #dc3545;
                        color: white;
                        border: none;
                        padding: 8px 16px;
                        cursor: pointer;
                        border-radius: 4px;
                        margin-top: 8px;
                        transition: background-color 0.3s;
                    }
                    .delete-btn:hover {
                        background-color: #c82333;
                    }
                    @media (max-width: 1200px) {
                        .image-item {
                            width: calc(25% - 40px); /* 4 images per row for medium screens */
                        }
                    }
                    @media (max-width: 900px) {
                        .image-item {
                            width: calc(33.33% - 40px); /* 3 images per row for small screens */
                        }
                    }
                    @media (max-width: 600px) {
                        .image-item {
                            width: calc(50% - 40px); /* 2 images per row for extra small screens */
                        }
                    }
                    @media (max-width: 400px) {
                        .image-item {
                            width: calc(100% - 40px); /* 1 image per row for very small screens */
                        }
                    }
                </style>
            </head>
            <body>
                <h1>Images for Class: ${className}</h1>
                <div class="image-container">
                    ${imageHtml}
                </div>
                <script>
                    document.addEventListener('DOMContentLoaded', () => {
                        // Add event listeners to all delete buttons
                        const deleteButtons = document.querySelectorAll('.delete-btn');
                        deleteButtons.forEach(button => {
                            button.addEventListener('click', async (event) => {
                                const imageId = event.target.dataset.imageId;
                                const type = event.target.dataset.type;
                                try {
                                    const response = await fetch('/delete_image', {
                                        method: 'POST',
                                        headers: {
                                            'Content-Type': 'application/json'
                                        },
                                        body: JSON.stringify({ imageId, type })
                                    });

                                    if (!response.ok) {
                                        throw new Error('Failed to delete image');
                                    }

                                    // Reload page or update UI after successful deletion
                                    window.location.reload(); // Example: reload the page
                                } catch (error) {
                                    console.error('Error deleting image:', error.message);
                                    alert('Failed to delete image');
                                }
                            });
                        });
                    });
                </script>
            </body>
            </html>
        `);
    });
});


app.post('/upload_unknown', upload.single('image'), (req, res) => {
    const { className } = req.body;
    const { filename, path: filePath } = req.file;
    const buffer = fs.readFileSync(filePath);


    // Check if the class name exists in the database
    connection.query('SELECT * FROM classes WHERE className = ?', [className], (err, results) => {
        if (err) {
            console.error('Database query error:', err);
            return res.status(500).send('Internal Server Error');
        }

        if (results.length > 0) {
            // Class exists, proceed with file handling and database insertion

            // Ensure the base images directory exists
            const baseImagesDir = path.join(__dirname, 'unknown_images');
            if (!fs.existsSync(baseImagesDir)) {
                fs.mkdirSync(baseImagesDir, { recursive: true });
            }

            // Create directory for class if not exists
            const classDir = path.join(baseImagesDir, className);
            if (!fs.existsSync(classDir)) {
                fs.mkdirSync(classDir, { recursive: true });
            }

            // Move uploaded file to class directory
            const newPath = path.join(classDir, filename);
            fs.renameSync(filePath, newPath);

            // Insert the image into the database
            connection.query('INSERT INTO unknown_photos (className, file_path , imageDb) VALUES (?, ? , ?)', [className, newPath , buffer], (err, result) => {
                if (err) {
                    console.error('Error inserting photo into database:', err);
                    return res.status(500).send('Internal Server Error');
                }
                console.log('Image uploaded and database updated');
                // Redirect to the detect page
               // res.redirect('/detect')
            });
        } else {
            // Class does not exist, delete the uploaded file and send an error response
            fs.unlinkSync(filePath); // Remove the temporary uploaded file
            console.error('Class does not exist in the database');
            return res.status(400).send('Class does not exist');
        }
    });
});


app.post('/display_unknown', (req, res) => {
    const { className } = req.body;

    connection.query('SELECT * FROM unknown_photos WHERE className = ? ORDER BY id DESC', [className], (err, results) => {
        if (err) {
            console.error('Database query error:', err);
            return res.status(500).send('Internal Server Error');
        }

        let imageHtml = '';
        results.forEach((image) => {
            // Generate HTML for each image item with a delete button
            imageHtml += `
                <div class="image-item">
                    <h3>Image for ${className}</h3>
                    <img src="data:image/jpeg;base64,${Buffer.from(image.imageDb).toString('base64')}" alt="${image.file_path}">
                    <br>
                    <button class="delete-btn" data-image-id="${image.id}" data-type="unknown">Delete</button>
                </div>
            `;
        });

        // Send HTML response with images and delete buttons
        res.send(`
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Images for Class: ${className}</title>
                <link rel="stylesheet" href="assets/display.css">
                <style>
                    .image-container {
                        display: flex;
                        flex-wrap: wrap;
                        gap: 20px;
                        justify-content: center;
                        padding: 20px;
                    }
                    .image-item {
                        background: white;
                        padding: 10px;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                        text-align: center;
                        width: calc(20% - 40px); /* Adjust width to display 5 images per row */
                        box-sizing: border-box;
                    }
                    .image-item img {
                        max-width: 100%;
                        height: auto;
                        border-radius: 5px;
                    }
                    .delete-btn {
                        background-color: #dc3545;
                        color: white;
                        border: none;
                        padding: 8px 16px;
                        cursor: pointer;
                        border-radius: 4px;
                        margin-top: 8px;
                        transition: background-color 0.3s;
                    }
                    .delete-btn:hover {
                        background-color: #c82333;
                    }
                    @media (max-width: 1200px) {
                        .image-item {
                            width: calc(25% - 40px); /* 4 images per row for medium screens */
                        }
                    }
                    @media (max-width: 900px) {
                        .image-item {
                            width: calc(33.33% - 40px); /* 3 images per row for small screens */
                        }
                    }
                    @media (max-width: 600px) {
                        .image-item {
                            width: calc(50% - 40px); /* 2 images per row for extra small screens */
                        }
                    }
                    @media (max-width: 400px) {
                        .image-item {
                            width: calc(100% - 40px); /* 1 image per row for very small screens */
                        }
                    }
                </style>
            </head>
            <body>
                <h1>Images for Class: ${className}</h1>
                <div class="image-container">
                    ${imageHtml}
                </div>
                <script>
                    document.addEventListener('DOMContentLoaded', () => {
                        // Add event listeners to all delete buttons
                        const deleteButtons = document.querySelectorAll('.delete-btn');
                        deleteButtons.forEach(button => {
                            button.addEventListener('click', async (event) => {
                                const imageId = event.target.dataset.imageId;
                                const type = event.target.dataset.type;
                                try {
                                    const response = await fetch('/delete_image', {
                                        method: 'POST',
                                        headers: {
                                            'Content-Type': 'application/json'
                                        },
                                        body: JSON.stringify({ imageId, type })
                                    });

                                    if (!response.ok) {
                                        throw new Error('Failed to delete image');
                                    }

                                    // Reload page or update UI after successful deletion
                                    window.location.reload(); // Example: reload the page
                                } catch (error) {
                                    console.error('Error deleting image:', error.message);
                                    alert('Failed to delete image');
                                }
                            });
                        });
                    });
                </script>
            </body>
            </html>
        `);
    });
});




// Delete image endpoint
app.post('/delete_image', (req, res) => {
    const { imageId, type } = req.body;

    let tableName;
    if (type === 'known') {
        tableName = 'images';
    } else if (type === 'unknown') {
        tableName = 'unknown_photos';
    } else {
        return res.status(400).send('Invalid image type');
    }

    // Perform deletion from the appropriate table in the database
    connection.query(`DELETE FROM ${tableName} WHERE id = ?`, [imageId], (err, results) => {
        if (err) {
            console.error('Error deleting image from database:', err);
            return res.status(500).send('Failed to delete image');
        }

        console.log(`Image with id ${imageId} deleted successfully from ${tableName} table.`);
        res.status(200).send('Image deleted successfully');
    });
});



app.post('/mark_attendance', (req, res) => {
    const className = req.body.className;

    if (!className) {
        return res.status(400).send('Class name is required');
    }

    const outputExcelFile = path.join(__dirname, 'attendance.xlsx');
    const pythonProcess = spawn('python', ['face_reco.py', className, outputExcelFile]);

    pythonProcess.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        if (code !== 0) {
            return res.status(500).send('Error marking attendance');
        }
        res.send('Attendance marked successfully');
    });
});

app.get('/download_attendance', (req, res) => {
    const className = req.query.className;
    const outputExcelFile = path.join(__dirname, 'attendance.xlsx');

    res.download(outputExcelFile, `${className}_attendance.xlsx`, (err) => {
        if (err) {
            console.error(`Error sending file: ${err.message}`);
            res.status(500).send('Error sending the attendance Excel file');
        } else {
            console.log('File sent successfully');
        }
    });
});



app.get('/logout', (req, res) => {
    res.clearCookie('session');
    res.redirect('/');
});

// Dashboard route
app.get('/welcome', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'welcome.html'));
});

app.get('/redirect-to-detect', (req, res) => {
    res.redirect('/detect'); // Redirect to the "/detect" route
});

// Route to serve the detection page
app.get('/detect', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'detect.html'));
});

// Route for the upload page
app.get('/upload', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'upload.html'));
});

// Route for the check page
app.get('/check', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'check.html'));
});


// Set app port
app.listen(4600, () => {
    console.log('Server is running on port 4600');
});
