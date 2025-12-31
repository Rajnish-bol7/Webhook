# Test curl commands for all WhatsApp message types

## 1. TEXT MESSAGE
curl --location 'http://localhost:8000/webhook/' \
--header 'Content-Type: application/json' \
--data '{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "356955237510870",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "918745097126",
              "phone_number_id": "432038163320755"
            },
            "contacts": [
              {
                "profile": {
                  "name": "Test User"
                },
                "wa_id": "918279486865"
              }
            ],
            "messages": [
              {
                "from": "918279486865",
                "id": "wamid.test123",
                "timestamp": "1766216432",
                "text": {
                  "body": "Hello from Postman!"
                },
                "type": "text"
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}'

## 2. AUDIO/VOICE MESSAGE
curl --location 'http://localhost:8000/webhook/' \
--header 'Content-Type: application/json' \
--data '{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "356955237510870",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "918745097126",
              "phone_number_id": "432038163320755"
            },
            "contacts": [
              {
                "profile": {
                  "name": "Test User"
                },
                "wa_id": "918279486865"
              }
            ],
            "messages": [
              {
                "from": "918279486865",
                "id": "wamid.audio123",
                "timestamp": "1766216635",
                "type": "audio",
                "audio": {
                  "mime_type": "audio/ogg; codecs=opus",
                  "sha256": "3d4yz0I+zNsq2LvInAgXp7R/odNwuJn1zQ1u/LbgeEA=",
                  "id": "24950395794663592",
                  "url": "https://lookaside.fbsbx.com/whatsapp_business/attachments/?mid=24950395794663592",
                  "voice": true
                }
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}'

## 3. IMAGE MESSAGE
curl --location 'http://localhost:8000/webhook/' \
--header 'Content-Type: application/json' \
--data '{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "356955237510870",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "918745097126",
              "phone_number_id": "432038163320755"
            },
            "contacts": [
              {
                "profile": {
                  "name": "Test User"
                },
                "wa_id": "918279486865"
              }
            ],
            "messages": [
              {
                "from": "918279486865",
                "id": "wamid.image123",
                "timestamp": "1766385276",
                "type": "image",
                "image": {
                  "mime_type": "image/jpeg",
                  "sha256": "T6BEw30Xo4q+n6mDy2jB+vIFrzltQaAu0LT+nk6k9zM=",
                  "id": "1482568382841964",
                  "url": "https://lookaside.fbsbx.com/whatsapp_business/attachments/?mid=1482568382841964",
                  "caption": "Test image caption"
                }
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}'

## 4. VIDEO MESSAGE
curl --location 'http://localhost:8000/webhook/' \
--header 'Content-Type: application/json' \
--data '{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "356955237510870",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "918745097126",
              "phone_number_id": "432038163320755"
            },
            "contacts": [
              {
                "profile": {
                  "name": "Test User"
                },
                "wa_id": "918279486865"
              }
            ],
            "messages": [
              {
                "from": "918279486865",
                "id": "wamid.video123",
                "timestamp": "1766391321",
                "type": "video",
                "video": {
                  "mime_type": "video/mp4",
                  "sha256": "E7T0lL0BD+pjg70BmFRlt5CYDSfRUfCjXoBEbOq+XCo=",
                  "id": "755279634255081",
                  "url": "https://lookaside.fbsbx.com/whatsapp_business/attachments/?mid=755279634255081",
                  "caption": "Test video caption"
                }
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}'

## 5. DOCUMENT MESSAGE
curl --location 'http://localhost:8000/webhook/' \
--header 'Content-Type: application/json' \
--data '{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "356955237510870",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "918745097126",
              "phone_number_id": "432038163320755"
            },
            "contacts": [
              {
                "profile": {
                  "name": "Test User"
                },
                "wa_id": "918279486865"
              }
            ],
            "messages": [
              {
                "from": "918279486865",
                "id": "wamid.doc123",
                "timestamp": "1766385465",
                "type": "document",
                "document": {
                  "filename": "test_document.pdf",
                  "mime_type": "application/pdf",
                  "sha256": "41cuvIKWgr2puK4VIFX6mR0TqePd5ACWDgVjT+USe4Y=",
                  "id": "871388365588153",
                  "url": "https://lookaside.fbsbx.com/whatsapp_business/attachments/?mid=871388365588153"
                }
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}'

## 6. LOCATION MESSAGE
curl --location 'http://localhost:8000/webhook/' \
--header 'Content-Type: application/json' \
--data '{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "356955237510870",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "918745097126",
              "phone_number_id": "432038163320755"
            },
            "contacts": [
              {
                "profile": {
                  "name": "Test User"
                },
                "wa_id": "918279486865"
              }
            ],
            "messages": [
              {
                "from": "918279486865",
                "id": "wamid.location123",
                "timestamp": "1766391591",
                "location": {
                  "latitude": 28.5771962,
                  "longitude": 77.3139617
                },
                "type": "location"
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}'

## 7. STICKER MESSAGE
curl --location 'http://localhost:8000/webhook/' \
--header 'Content-Type: application/json' \
--data '{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "356955237510870",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "918745097126",
              "phone_number_id": "432038163320755"
            },
            "contacts": [
              {
                "profile": {
                  "name": "Test User"
                },
                "wa_id": "918279486865"
              }
            ],
            "messages": [
              {
                "from": "918279486865",
                "id": "wamid.sticker123",
                "timestamp": "1766391633",
                "type": "sticker",
                "sticker": {
                  "mime_type": "image/webp",
                  "sha256": "t+uy7KqE5MJ55oQWEUW5XwN8QoMLUIzPHBMrSjZakLo=",
                  "id": "1975870883305819",
                  "url": "https://lookaside.fbsbx.com/whatsapp_business/attachments/?mid=1975870883305819",
                  "animated": false
                }
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}'

## 8. CONTACTS MESSAGE
curl --location 'http://localhost:8000/webhook/' \
--header 'Content-Type: application/json' \
--data '{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "356955237510870",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "918745097126",
              "phone_number_id": "432038163320755"
            },
            "contacts": [
              {
                "profile": {
                  "name": "Test User"
                },
                "wa_id": "918279486865"
              }
            ],
            "messages": [
              {
                "from": "918279486865",
                "id": "wamid.contacts123",
                "timestamp": "1766391474",
                "type": "contacts",
                "contacts": [
                  {
                    "name": {
                      "first_name": "Anil",
                      "middle_name": "Sir",
                      "last_name": "Bol7",
                      "formatted_name": "Anil Sir Bol7"
                    },
                    "phones": [
                      {
                        "phone": "+91 93131 55788",
                        "wa_id": "919313155788",
                        "type": "MOBILE"
                      }
                    ]
                  }
                ]
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}'
