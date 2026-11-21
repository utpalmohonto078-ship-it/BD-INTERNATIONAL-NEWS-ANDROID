package com.bdinternationalnews.app

import android.app.Activity
import android.os.Bundle
import android.graphics.Typeface
import android.view.Gravity
import android.view.View
import android.widget.*
import org.json.JSONArray
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import java.util.concurrent.Executors

class MainActivity : Activity() {
    private val server = "https://bd-international-news.onrender.com"
    private val executor = Executors.newSingleThreadExecutor()
    private lateinit var output: TextView
    private lateinit var status: TextView
    private lateinit var list: LinearLayout

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(18, 22, 18, 18)
        }

        val heading = TextView(this).apply {
            text = "BD INTERNATIONAL NEWS"
            textSize = 23f
            typeface = Typeface.DEFAULT_BOLD
        }
        root.addView(heading)

        status = TextView(this).apply {
            text = "বাংলাদেশ থেকে বিশ্ব, সত্যের সন্ধানে।"
            textSize = 14f
            setPadding(0, 12, 0, 14)
        }
        root.addView(status)

        val refresh = Button(this).apply {
            text = "সংবাদ আপডেট"
            setOnClickListener { loadNews() }
        }
        root.addView(refresh)

        val scroll = ScrollView(this)
        list = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
        }
        scroll.addView(list)
        root.addView(scroll, LinearLayout.LayoutParams(-1, 0, 1f))

        output = TextView(this).apply {
            textSize = 15f
            setPadding(0, 12, 0, 12)
        }
        list.addView(output)

        val footer = TextView(this).apply {
            text = "BANGLADESH BHASHA • BD INTERNATIONAL NEWS"
            textSize = 11f
            gravity = Gravity.CENTER
        }
        root.addView(footer)

        setContentView(root)
        loadNews()
    }

    private fun loadNews() {
        status.text = "সার্ভারের সঙ্গে সংযোগ হচ্ছে..."
        output.text = "সংবাদ লোড হচ্ছে..."

        executor.execute {
            var connection: HttpURLConnection? = null
            try {
                connection = URL("$server/api/news").openConnection()
                    as HttpURLConnection
                connection.requestMethod = "GET"
                connection.connectTimeout = 15000
                connection.readTimeout = 20000
                connection.setRequestProperty("Accept", "application/json")

                val code = connection.responseCode
                val stream = if (code in 200..299)
                    connection.inputStream else connection.errorStream
                val body = stream?.bufferedReader()?.use { it.readText() } ?: ""

                runOnUiThread {
                    status.text = "সার্ভার HTTP $code"
                    renderResponse(body, code)
                }
            } catch (e: Exception) {
                runOnUiThread {
                    status.text = "সার্ভার সংযোগ ব্যর্থ"
                    output.text = "সংবাদ API পাওয়া যায়নি:\n${e.message}\n\nAPI path: /api/news"
                }
            } finally {
                connection?.disconnect()
            }
        }
    }

    private fun renderResponse(body: String, code: Int) {
        list.removeAllViews()
        if (code !in 200..299) {
            output = TextView(this).apply {
                text = "API উত্তর: HTTP $code\n${body.take(3000)}"
                textSize = 14f
            }
            list.addView(output)
            return
        }

        try {
            val items = when {
                body.trimStart().startsWith("[") -> JSONArray(body)
                else -> {
                    val obj = JSONObject(body)
                    when {
                        obj.opt("articles") is JSONArray -> obj.getJSONArray("articles")
                        obj.opt("data") is JSONArray -> obj.getJSONArray("data")
                        else -> JSONArray()
                    }
                }
            }

            if (items.length() == 0) {
                output.text = "সার্ভার সংযুক্ত। সংবাদ তালিকার API response format যাচাই প্রয়োজন।\n\n${body.take(2500)}"
                list.addView(output)
                return
            }

            for (i in 0 until items.length()) {
                val item = items.optJSONObject(i) ?: continue
                val title = item.optString("title", "শিরোনাম নেই")
                val content = item.optString("body",
                    item.optString("summary", item.optString("description", "")))

                val card = TextView(this).apply {
                    text = "$title\n\n$content"
                    textSize = 16f
                    setPadding(12, 16, 12, 16)
                }
                list.addView(card)
                val divider = View(this).apply {
                    setBackgroundColor(0xFFDDDDDD.toInt())
                }
                list.addView(divider, LinearLayout.LayoutParams(-1, 1))
            }
        } catch (e: Exception) {
            output.text = "API JSON বিশ্লেষণ করা যায়নি:\n${e.message}\n\n${body.take(2500)}"
            list.addView(output)
        }
    }

    override fun onDestroy() {
        executor.shutdown()
        super.onDestroy()
    }
}
