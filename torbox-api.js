const fs = require('fs')
const url = require('url')
const path = require('path')
const request = require('request')
const express = require('express')

const app = express()

const port = 4004
const key = 'Yy?@wV%PN+q#RBp+wyUHDLRv$L@8=@H?'
const downloadDir = path.join(__dirname, '/testing/downloads/')

// Middleware to process body json from post requests
app.use(express.json()) 

app.post('/addTorrent', (req, res) => {
    // Check key
    if (req.body.key != key) { res.status(403).send(); return }
    // Guarantee url is at least included
    if (!req.body.url) { res.status(400).send(); return }

    // Try to download file from url
    fileURL = req.body.url
    var requestFile = request(fileURL).on('response', (request_res) => {

        if (request_res.statusCode == 404) { res.status(404).send(); return }
        var filename, contentDisp = request_res.headers['content-disposition']
        if (contentDisp && /^attachment/i.test(contentDisp)) {
            filename = contentDisp
                .split('filename=')[1]
                .split(';')[0]
                .replace(/"/g, '')
        } else {
            filename = path.basename(url.parse(fileURL).path)
        }

        requestFile.pipe(fs.createWriteStream(path.join(downloadDir, filename))
            .on('error', (err) => {
                res.status(500).send()
            })
            .on('close', () => {
                res.status(200).send()
            }))

    })

})

app.listen(port, () => {
    console.log(`Torrent API running on port ${port}.`)
})